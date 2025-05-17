# python module3.py

import asyncio
import json
import os
import logging
import datetime
import re
from typing import Any, List, Dict, Tuple, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

from agents import Agent, GuardrailFunctionOutput, OutputGuardrail, Runner
from agents.run_context import RunContextWrapper
from agents.lifecycle import AgentHooks

load_dotenv()  # Load environment variables

# --- Setup Logging --- (Your original verbose logging setup)
def setup_logging(module_name):
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(logs_dir, f"{module_name}_{timestamp}.log")
    verbose_log_file = os.path.join(logs_dir, f"{module_name}_verbose_{timestamp}.log")

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        logger.handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Verbose logger (no truncation)
    verbose_logger = logging.getLogger(f"{module_name}_verbose")
    verbose_logger.setLevel(logging.INFO)
    if verbose_logger.handlers:
        verbose_logger.handlers = []
    verbose_file_handler = logging.FileHandler(verbose_log_file)
    verbose_file_handler.setLevel(logging.INFO)
    verbose_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    verbose_file_handler.setFormatter(verbose_format)
    verbose_logger.addHandler(verbose_file_handler)

    return logger, verbose_logger

logger, verbose_logger = setup_logging("module3")

def log_info(message, truncate=False, max_length=5000):
    verbose_logger.info(message)  # Always log full message to verbose
    if truncate:
        if len(message) > max_length:
            message = message[:max_length] + "... [truncated, see verbose log]"
        logger.info(message)
    else:
        logger.info(message)

# --- Text Validation Functions --- (No changes)
def sanitize_text(text: str) -> str:
    """Clean and validate text to prevent corruption."""
    if not isinstance(text, str):
        return str(text)
    text = ''.join(char for char in text if char.isprintable() or char in ['\n', '\t', ' '])
    corruption_pattern = r'[\u0400-\u04FF\u0600-\u06FF\u0900-\u097F\u3040-\u309F\u30A0-\u30FF\u3130-\u318F\uAC00-\uD7AF]{3,}'
    text = re.sub(corruption_pattern, '[corrupted text removed]', text)
    max_length = 50000
    if len(text) > max_length:
        text = text[:max_length] + "...[text truncated due to length]"
    return text

# --- Custom Agent Hooks for Detailed Logging --- (Modified for verbose logging)
class DetailedLoggingHooks(AgentHooks):
    def __init__(self, logger, verbose_logger):
        self.logger = logger
        self.verbose_logger = verbose_logger  # Use both loggers

    async def on_start(
        self, context: RunContextWrapper[Any], agent: Agent
    ):
        """Log details before LLM generation."""
        log_info(f"===== API CALL: {agent.name} =====")
        log_info(f"Starting agent: {agent.name}")
        return

    async def on_end(
        self, context: RunContextWrapper[Any], agent: Agent, output: Any
    ):
        """Log details after LLM generation, with sanitization."""
        log_info(f"===== API RESPONSE: {agent.name} =====", truncate=True)
        self.verbose_logger.info(f"===== API RESPONSE: {agent.name} =====")
        try:
            if hasattr(output, 'final_output'):
                # Handle different response types, sanitizing text fields
                if hasattr(output.final_output, 'expanded_text'):
                    output.final_output.expanded_text = sanitize_text(output.final_output.expanded_text)
                elif hasattr(output.final_output, 'reasoning'): #For EvalResult
                    output.final_output.reasoning = sanitize_text(output.final_output.reasoning)
                if hasattr(output.final_output, 'improvement_suggestions'):
                    output.final_output.improvement_suggestions = [sanitize_text(s) for s in output.final_output.improvement_suggestions]
                response_content = json.dumps(output.final_output, indent=2)
                log_info(f"Response from {agent.name}: {response_content}", truncate=True)
                self.verbose_logger.info(f"Response from {agent.name}: {response_content}") # Full response
            else:
                log_info(f"Response from {agent.name}: {str(output)}", truncate=True)
                self.verbose_logger.info(f"Response from {agent.name}: {str(output)}")
        except Exception as e:
            log_info(f"Response from {agent.name}: {str(output)}", truncate=True)
            log_info(f"Could not format response as JSON: {e}", truncate=True)
            self.verbose_logger.info(f"Response from {agent.name}: {str(output)}")
            self.verbose_logger.info(f"Could not format response as JSON: {e}")

        return output

    async def on_tool_start(
        self, context: RunContextWrapper[Any], agent: Agent, tool: Any
    ):
        """Called before a tool is invoked."""
        log_info(f"===== TOOL CALL: {agent.name} =====")
        self.verbose_logger.info(f"===== TOOL CALL: {agent.name} =====") # Redundant, but consistent
        return


    async def on_tool_end(
        self, context: RunContextWrapper[Any], agent: Agent, tool: Any, result: str
    ):
        """Called after a tool is invoked."""
        # Always log full to verbose, optionally truncate regular log
        self.verbose_logger.info(f"Tool result for {agent.name}: {result}")
        log_info(f"Tool result for {agent.name}: {result}", truncate=True, max_length=1000)
        return result

logging_hooks = DetailedLoggingHooks(logger, verbose_logger)

# --- Pydantic Models --- (EvalResult Modified)
class SuccessCriteria(BaseModel):
    criteria: str
    reasoning: str
    rating: int = Field(..., description="Rating of the criterion (1-10)")

    @field_validator('rating')
    def check_rating(cls, v):
        if not 1 <= v <= 10:
            raise ValueError('Rating must be between 1 and 10')
        return v

class PlanItem(BaseModel):
    item_title: str = Field(..., description="A concise title for this plan item.")
    item_description: str = Field(..., description="A description of this step in the plan.")

class PlanOutline(BaseModel):
    plan_title: str = Field(..., description="A title for the overall plan.")
    plan_description: str = Field(..., description="A brief summary of the plan approach")
    plan_items: list[PlanItem] = Field(..., description="A list of plan items.")
    reasoning: str = Field(..., description="Reasoning for why this plan is suitable.")
    rating: int = Field(..., description="Rating of the plan's suitability (1-10).")
    created_by: str = Field(..., description="The name of the agent that created this plan")

    @field_validator('plan_items')
    def check_plan_items(cls, v):
        if len(v) < 3:
            raise ValueError('Must provide at least three plan items')
        return v

    @field_validator('rating')
    def check_rating(cls, v):
        if not 1 <= v <= 10:
            raise ValueError('Rating must be between 1 and 10')
        return v

class Module2Output(BaseModel):  # For loading the JSON
    goal: str
    selected_criteria: list[SuccessCriteria]  # Updated to list
    plan_outlines: list[PlanOutline]
    selected_outline: PlanOutline

class ExpandedItem(BaseModel):
    expanded_text: str = Field(..., description="The detailed, multi-paragraph expansion of the plan item.")

    @field_validator('expanded_text')
    def validate_text(cls, v):
        """Validate and sanitize expanded text."""
        return sanitize_text(v)

# --- REVISED EvalResult Model ---
class EvalResult(BaseModel):
    result: str = Field(..., description="Overall result: 'pass' or 'fail'.  Fail if the rating is below 3.")
    reasoning: str = Field(..., description="CRITICAL evaluation: Explain WHY the result is 'pass' or 'fail'.  Identify specific WEAKNESSES, even if passing.")
    criteria: SuccessCriteria = Field(..., description="The success criterion being evaluated against.")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5, 5=perfect)")  # 1-5 scale
    improvement_suggestions: List[str] = Field(..., min_items=1, description="Specific suggestions for improvement.")

    @field_validator('result')
    def check_result(cls, v):
        if v.lower() not in ["pass", "fail"]:
            raise ValueError("Result must be 'pass' or 'fail'")
        return v.lower()

    @field_validator('reasoning')
    def validate_reasoning(cls, v):
        return sanitize_text(v)
      
    @field_validator('improvement_suggestions')
    def validate_suggestions(cls, v):
        if len(v) < 1:
            raise ValueError('Must provide at least one suggestion')
        return v

class Module3Output(BaseModel):
    goal: str
    selected_criteria: list[SuccessCriteria]
    selected_outline: PlanOutline
    expanded_outline: PlanOutline
    evaluation_results: list[EvalResult]  # List of EvalResult objects (one per item)
    criteria_summary: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Summary of pass/fail, and average ratings"
    )

# --- Agents --- (evaluate_item_agent instructions MODIFIED)
expand_item_agent = Agent(
    name="ItemExpander",
    instructions=(
        "You are a detailed planner. Given a goal, multiple success criteria, a plan outline, "
        "and a specific plan item title and description, expand that plan item into a "
        "detailed, multi-paragraph description. Be thorough and specific. "
        "Make sure your expansion addresses all of the success criteria provided. "
        "Your expanded text should be comprehensive and actionable within a reasonable length (max 3000 words)."
    ),
    model="gpt-4o",
    output_type=ExpandedItem,
    hooks=logging_hooks,
)


# MODIFIED AGENT: ItemEvaluator (now a synthesis agent)
evaluate_item_agent = Agent(
    name="ItemEvaluator",
    instructions=(
        """You are a STRICT and CRITICAL plan evaluator. Given a goal, a specific success criterion,
        a full plan outline, and a detailed expansion of a single plan item, evaluate whether that
        expanded item *FULLY* meets the specified success criterion, in the context of the overall plan and goal.

        Output ONLY 'pass' or 'fail' in the 'result' field.  'pass' ONLY if the criterion is COMPLETELY met (a rating of 4 or 5).  'fail' if there are ANY weaknesses.

        Provide DETAILED reasoning, EXPLICITLY identifying any weaknesses, gaps, or areas where the expanded item could be improved to BETTER meet the criterion. Even if you 'pass' the item, suggest improvements.

        Give a numerical rating from 1 to 5, where:
        1 = Poor (Fails to address the criterion in any meaningful way)
        2 = Below Average (Addresses some aspects, but has MAJOR gaps or issues)
        3 = Average (Addresses the criterion adequately, but with notable weaknesses)
        4 = Good (Addresses the criterion well, with only minor weaknesses)
        5 = Excellent (COMPLETELY addresses the criterion with NO significant weaknesses)

        Be HARSH in your ratings.  A '5' should be RARE.

        You MUST provide at least ONE specific, actionable suggestion for improvement, even if the item passes.

        Your output MUST follow this JSON structure:
        {
          "result": "pass" or "fail",
          "reasoning": "...",  // CRITICAL evaluation and justification
          "criteria": { ... }, // The criterion object
          "rating": 1,       // The 1-5 rating
          "improvement_suggestions": ["...", "..."] // At least one suggestion
        }

        Here are examples of proper evaluations (DO NOT COPY EXACTLY, adapt to the specific context):

        Example 1 (FAIL):

        ```json
        {
          "result": "fail",
          "reasoning": "While the expanded item mentions user engagement, it focuses primarily on features and not on strategies to *actively* increase engagement by 10% monthly.  It lacks concrete, measurable steps.  The 'Surprise Me' button is mentioned, but its impact on growth isn't quantified. The plan doesn't address how new users will be acquired.",
          "criteria": {
            "criteria": "Active Users Growth (10% monthly increase)",
            "reasoning": "...",
            "rating": 9
          },
           "rating": 2,
         "improvement_suggestions": ["Add a section on marketing and user acquisition.", "Define specific, measurable, achievable, relevant, and time-bound (SMART) goals for user growth."]
        }
        ```

        Example 2 (PASS, but with suggestions):

        ```json
        {
          "result": "pass",
          "reasoning": "The item addresses data privacy by mentioning encryption and compliance with regulations. However, it's somewhat general and could be more specific about the *types* of encryption used and the *exact* regulations followed.",
          "criteria": {
            "criteria": "Compliance with Data Privacy Standards",
            "reasoning": "...",
            "rating": 10
          },
          "rating": 4,
          "improvement_suggestions": ["Specify the encryption standards (e.g., AES-256).", "Explicitly name GDPR and CCPA compliance.", "Outline a process for regular data privacy audits."]
        }
        ```

        Evaluate the following.  Remember to be STRICT and CRITICAL.
        """
    ),
    model="gpt-4o",
    output_type=EvalResult,  # Uses the MODIFIED EvalResult
    hooks=logging_hooks,
)

# --- Validation Function --- (No changes)
async def validate_module3_output(
    context: RunContextWrapper[None], agent: Agent, agent_output: Any
) -> GuardrailFunctionOutput:
    """Validates the output of Module 3."""
    try:
        logger.info("Validating Module 3 output...")
        truncated_output = {k: v for k, v in agent_output.model_dump().items() if k != 'expanded_outline'}
        logger.info(f"Output to validate (truncated): {json.dumps(truncated_output, indent=2)}")
        Module3Output.model_validate(agent_output)
        logger.info("Module 3 output validation passed")
        return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)
    except ValidationError as e:
        logger.error(f"Module 3 output validation failed: {e}")
        return GuardrailFunctionOutput(
            output_info={"error": str(e)}, tripwire_triggered=True
        )

# ---  Processing Function --- (Modified to use new EvalResult)
async def process_item(
    goal: str,
    success_criteria: list[SuccessCriteria],
    plan_outline: PlanOutline,
    item: PlanItem,
    context: RunContextWrapper[None],
    item_index: int,
) -> tuple[PlanItem, list[EvalResult]]:
    """Expands and evaluates a single plan item against all success criteria."""
    logger.info(f"Processing plan item {item_index+1}: {item.item_title}")
    
    # Format all criteria for input
    criteria_text = "\n".join([f"- {c.criteria}" for c in success_criteria])
    
    # Expand the item
    logger.info(f"Expanding item: {item.item_title}")
    expand_input = (
        f"Goal: {goal}\n"
        f"Success Criteria:\n{criteria_text}\n"
        f"Plan Outline: {plan_outline.plan_title}\n"
        f"Plan Description: {plan_outline.plan_description}\n"
        f"Item to Expand:\nTitle: {item.item_title}\nDescription: {item.item_description}"
    )
    
    expand_result = await Runner.run(
        expand_item_agent,
        input=expand_input,
        context=context,
    )
    expanded_item_text = expand_result.final_output.expanded_text
    expanded_item_text = sanitize_text(expanded_item_text)
    logger.info(f"Item expanded to {len(expanded_item_text)} characters")

    expanded_item = PlanItem(item_title=item.item_title, item_description=expanded_item_text)
    logger.info(f"Evaluating expanded item against {len(success_criteria)} criteria")
    eval_results = []

    for i, criterion in enumerate(success_criteria):
        logger.info(f"Evaluating against criterion {i+1}: {criterion.criteria}")

        # Create evaluation input focusing on this specific criterion
        evaluation_input = (
            f"Goal: {goal}\n\n"
            f"Success Criterion: {criterion.criteria}\n"
            f"Criterion Reasoning: {criterion.reasoning}\n"
            f"Original Criterion Rating: {criterion.rating}\n"
            f"Full Plan Outline: \n{json.dumps(plan_outline.model_dump(), indent=2)}\n"
            f"Expanded Item: {expanded_item_text}\n\n"
            f"Evaluate ONLY how well this expanded item addresses THIS SPECIFIC criterion.\n"
            f"Be STRICT and CRITICAL in your evaluation. Identify SPECIFIC strengths and weaknesses.\n"
            f"Provide concrete suggestions for improvement even if the item generally meets the criterion."
        )
        log_info(f"Evaluation input for criterion {i+1} (truncated): {evaluation_input[:5000]}...", 
                truncate=True, max_length=5000)
        verbose_logger.info(f"Full evaluation input for criterion {i+1}: {evaluation_input}")

        evaluation_result = await Runner.run(
            evaluate_item_agent,
            input=evaluation_input,
            context=context,
        )

        result = evaluation_result.final_output

        #If criteria is missing add it
        result_dict = result.model_dump()
        if 'criteria' not in result_dict or not result_dict['criteria']:
          result_dict['criteria'] = criterion.model_dump()
          result = EvalResult.model_validate(result_dict)

        result.reasoning = sanitize_text(result.reasoning) #Sanitize
        eval_results.append(result)

        logger.info(f"Evaluation result for criterion {i+1}: {result.result} - Rating: {result.rating}/5")

    return expanded_item, eval_results

# --- MODIFIED Summary Function ---
def generate_criteria_summary(evaluation_results: list[EvalResult]) -> Dict[str, Dict[str, Any]]:
    """Generate a summary of how items performed against each criterion, including average ratings."""
    summary = {}

    for result in evaluation_results:
      criterion_name = result.criteria.criteria
      if criterion_name not in summary:
          summary[criterion_name] = {"pass": 0, "fail": 0, "total": 0, "ratings": []}

      summary[criterion_name][result.result] += 1
      summary[criterion_name]["total"] += 1
      summary[criterion_name]["ratings"].append(result.rating)  # Collect ratings

    # Calculate average rating for each criterion
    for criterion_data in summary.values():
      if criterion_data["total"] > 0:
          criterion_data["average_rating"] = round(sum(criterion_data["ratings"]) / criterion_data["total"], 2)
      else:
            criterion_data["average_rating"] = 0  # Handle case where no ratings exist
      del criterion_data["ratings"] #Remove raw ratings

    return summary

# --- Main Module Function --- (No changes)
async def run_module_3(input_file: str, output_file: str) -> None:
    """Runs Module 3."""
    context = RunContextWrapper(context=None)

    try:
        logger.info(f"Starting Module 3, reading input from {input_file}")
        with open(input_file, "r") as f:
            module_2_data = json.load(f)
            logger.info(f"Successfully loaded data from {input_file}")

        module_2_output = Module2Output.model_validate(module_2_data)
        goal = module_2_output.goal
        selected_criteria = module_2_output.selected_criteria
        selected_plan = module_2_output.selected_outline

        logger.info(f"Goal: {goal}")
        logger.info(f"Number of selected criteria: {len(selected_criteria)}")
        logger.info(f"Selected plan: {selected_plan.plan_title}")

        logger.info("Processing all plan items...")
        expanded_plan_items = []
        all_eval_results = []  # This now stores EvalResult objects

        for i, item in enumerate(selected_plan.plan_items):
            expanded_item, item_eval_results = await process_item(
                goal=goal,
                success_criteria=selected_criteria,
                plan_outline=selected_plan,
                item=item,
                context=context,
                item_index=i,
            )

            expanded_plan_items.append(expanded_item)
            all_eval_results.extend(item_eval_results)  # Append EvalResult object
            logger.info(f"Completed processing item {i+1}: {item.item_title}")


        logger.info("Creating expanded outline with expanded items")
        expanded_outline = PlanOutline(
            plan_title=selected_plan.plan_title,
            plan_description=selected_plan.plan_description,
            plan_items=expanded_plan_items,
            reasoning=selected_plan.reasoning,
            rating=selected_plan.rating,
            created_by=selected_plan.created_by
        )

        criteria_summary = generate_criteria_summary(all_eval_results)  # Pass EvalResult objects
        logger.info(f"Criteria summary: {json.dumps(criteria_summary, indent=2)}")

        logger.info("Creating Module 3 output object")
        module_3_output = Module3Output(
            goal=goal,
            selected_criteria=selected_criteria,
            selected_outline=selected_plan,
            expanded_outline=expanded_outline,
            evaluation_results=all_eval_results,    # All evaluation results
            criteria_summary=criteria_summary,      # Summary of results
        )

        logger.info("Applying output guardrail...")
        guardrail = OutputGuardrail(guardrail_function=validate_module3_output)
        guardrail_result = await guardrail.run(
            agent=evaluate_item_agent,  # The LAST agent that ran
            agent_output=module_3_output,
            context=context,
        )

        if guardrail_result.output.tripwire_triggered:
            logger.error(f"Guardrail failed: {guardrail_result.output.output_info}")
            verbose_logger.error(f"Guardrail failed: {guardrail_result.output.output_info}")
            return  # Exit if validation fails
        # --- Smart JSON Export ---
        # Create data directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # Create timestamped version
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.basename(output_file)
        name, ext = os.path.splitext(filename)
        timestamped_file = os.path.join(output_dir, f"{name}_{timestamp}{ext}")
        
        # Export both versions
        with open(output_file, "w") as f:
            json.dump(module_3_output.model_dump(), f, indent=4)
        with open(timestamped_file, "w") as f:
            json.dump(module_3_output.model_dump(), f, indent=4)
        
        logger.info(f"Module 3 completed. Output saved to {output_file}")
        logger.info(f"Timestamped output saved to {timestamped_file}")

    except Exception as e:
        logger.error(f"An error occurred in Module 3: {e}")
        verbose_logger.error(f"An error occurred in Module 3: {e}")
        import traceback
        error_trace = traceback.format_exc()
        logger.error(error_trace)
        verbose_logger.error(error_trace)  # Log the full stack trace

async def main():
    logger.info("Starting main function")
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    input_file = os.path.join(input_dir, "module2_output.json")
    output_file = os.path.join(input_dir, "module3_output.json")
    await run_module_3(input_file, output_file)
    logger.info("Main function completed")

if __name__ == "__main__":
    logger.info("Module 3 script starting")
    asyncio.run(main())
    logger.info("Module 3 script completed")
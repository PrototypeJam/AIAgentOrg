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

# --- Setup Logging ---
def setup_logging(module_name):
    """Set up logging to both console and file."""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create a timestamp for the log filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(logs_dir, f"{module_name}_{timestamp}.log")
    
    # Create a verbose log file that captures everything without truncation
    verbose_log_file = os.path.join(logs_dir, f"{module_name}_verbose_{timestamp}.log")
    
    # Configure logging
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # Verbose file handler (same level, but we won't truncate messages logged to this)
    verbose_file_handler = logging.FileHandler(verbose_log_file)
    verbose_file_handler.setLevel(logging.INFO)
    verbose_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    verbose_file_handler.setFormatter(verbose_format)
    
    # Create a separate logger for verbose logging
    verbose_logger = logging.getLogger(f"{module_name}_verbose")
    verbose_logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    if verbose_logger.handlers:
        verbose_logger.handlers = []
    
    verbose_logger.addHandler(verbose_file_handler)
    
    return logger, verbose_logger

# Initialize loggers
logger, verbose_logger = setup_logging("module3")

# Helper function to log both normal and verbose
def log_info(message, truncate=False, max_length=None):
    """Log to both normal and verbose logs, with optional truncation for normal log."""
    # Always log full message to verbose log
    verbose_logger.info(message)
    
    # Optionally truncate for normal log
    if truncate and max_length and len(message) > max_length:
        truncated = message[:max_length] + f"... [truncated, full message in verbose log]"
        logger.info(truncated)
    else:
        logger.info(message)

# --- Text Validation Functions ---
def sanitize_text(text: str) -> str:
    """Clean and validate text to prevent corruption."""
    if not isinstance(text, str):
        return str(text)
        
    # Remove any non-printable or control characters
    text = ''.join(char for char in text if char.isprintable() or char in ['\n', '\t', ' '])
    
    # Check for obvious corruption patterns (random Unicode characters, etc.)
    # This regex looks for clusters of non-English characters that might indicate corruption
    corruption_pattern = r'[\u0400-\u04FF\u0600-\u06FF\u0900-\u097F\u3040-\u309F\u30A0-\u30FF\u3130-\u318F\uAC00-\uD7AF]{3,}'
    
    # Replace corrupted sections with a note
    text = re.sub(corruption_pattern, '[corrupted text removed]', text)
    
    # Ensure the text doesn't exceed a reasonable size (50KB)
    max_length = 50000
    if len(text) > max_length:
        text = text[:max_length] + "...[text truncated due to length]"
    
    return text

# --- Custom Agent Hooks for Detailed Logging ---
class DetailedLoggingHooks(AgentHooks):
    def __init__(self, logger, verbose_logger):
        self.logger = logger
        self.verbose_logger = verbose_logger

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
        """Log details after LLM generation."""
        log_info(f"===== API RESPONSE: {agent.name} =====")
        
        # Format the response for better readability
        try:
            if hasattr(output, 'final_output'):
                # For expanded items, sanitize the text
                if hasattr(output.final_output, 'expanded_text'):
                    output.final_output.expanded_text = sanitize_text(output.final_output.expanded_text)
                
                response_content = json.dumps(output.final_output, indent=2) 
                log_info(f"Response from {agent.name}: {response_content}", truncate=True, max_length=5000)
            else:
                log_info(f"Response from {agent.name}: {str(output)}")
        except Exception as e:
            log_info(f"Response from {agent.name}: {str(output)}")
            log_info(f"Could not format response as JSON: {e}")
        return output

    async def on_tool_start(
        self, context: RunContextWrapper[Any], agent: Agent, tool: Any
    ):
        """Called before a tool is invoked."""
        log_info(f"Tool being called by {agent.name}: {tool}")
        return

    async def on_tool_end(
        self, context: RunContextWrapper[Any], agent: Agent, tool: Any, result: str
    ):
        """Called after a tool is invoked."""
        log_info(f"Tool result for {agent.name}: {result}", truncate=True, max_length=5000)
        return result

# Create logging hooks
logging_hooks = DetailedLoggingHooks(logger, verbose_logger)

# --- Few-Shot Examples for Evaluation ---
PASS_EXAMPLE = """
Criterion: The plan must be cost-effective with a clear ROI
Item: Budget allocation and financial tracking

Evaluation:
- Strengths: 
  1. Includes detailed budget breakdown
  2. Mentions ROI tracking mechanisms
- Weaknesses:
  1. No contingency planning for budget overruns
  2. Lacks specific ROI calculation methodology
- Rating: 3/5 - Addresses the criterion well but has clear areas for improvement
- Result: PASS

Reasoning: This item PASSES because it establishes both budget controls and ROI tracking, which directly fulfill the criterion. The 3/5 rating reflects that while the core requirements are met, the item could be strengthened by adding contingency planning and specific ROI calculation methods.
"""

FAIL_EXAMPLE = """
Criterion: The solution must accommodate users with disabilities
Item: User interface design

Evaluation:
- Strengths:
  1. Mentions clean, intuitive interface
  2. Includes user testing feedback process
- Weaknesses:
  1. No specific accessibility features mentioned
  2. Doesn't address different types of disabilities
  3. No compliance with accessibility standards cited
- Rating: 2/5 - Major gaps in addressing accessibility requirements
- Result: FAIL

Reasoning: This item FAILS because it doesn't adequately address the core requirement of accommodating users with disabilities. While the UI design includes good general practices, it lacks specific accessibility features, doesn't consider different disability types, and doesn't reference compliance standards like WCAG. These are critical omissions for this criterion.
"""

# --- Pydantic Models ---
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

# New models for improved evaluation - FIXED TO REMOVE MIN_ITEMS VALIDATION
class CriterionStrengthWeakness(BaseModel):
    strengths: List[str] = Field(..., description="Strengths of the item for this criterion")
    weaknesses: List[str] = Field(..., description="Weaknesses of the item for this criterion")
    rating: int = Field(..., ge=1, le=5, description="Rating on a scale of 1-5")
    justification: str = Field(..., description="Detailed justification for the rating")

class EvalResult(BaseModel):
    result: str = Field(..., description="Either 'pass' or 'fail'")
    reasoning: str = Field(..., description="The evaluator's reasoning")
    criteria: SuccessCriteria = Field(..., description="The success criterion being evaluated against")
    strengths_weaknesses: CriterionStrengthWeakness = Field(..., description="Detailed strengths and weaknesses analysis")
    improvement_suggestions: List[str] = Field(..., description="Specific suggestions for improvement")

    @field_validator('result')
    def check_result(cls, v):
        if v.lower() not in ["pass", "fail"]:
            raise ValueError("Result must be 'pass' or 'fail'")
        return v.lower()
    
    @field_validator('reasoning')
    def validate_reasoning(cls, v):
        """Validate and sanitize reasoning text."""
        return sanitize_text(v)
    
# --- Module 3 Output ---
class Module3Output(BaseModel):
    goal: str
    selected_criteria: list[SuccessCriteria]  # Updated to list
    selected_outline: PlanOutline  # Original outline
    expanded_outline: PlanOutline  # Outline with expanded items
    evaluation_results: list[EvalResult]  # List of results for all criteria
    criteria_summary: Dict[str, Dict[str, int]] = Field(
        default_factory=dict, description="Summary of pass/fail counts per criterion"
    )

# --- Agents ---
expand_item_agent = Agent(
    name="ItemExpander",
    instructions=(
        "You are a detailed planner. Given a goal, multiple success criteria, a plan outline, "
        "and a specific plan item title and description, expand that plan item into a "
        "detailed, multi-paragraph description. Be thorough and specific. "
        "Make sure your expansion addresses all of the success criteria provided. "
        "Your expanded text should be comprehensive and actionable. "
        "Include specific actions, methods, tools, or techniques where appropriate. "
        "Keep your response within a reasonable length (maximum 3000 words) to ensure it can be "
        "processed effectively."
    ),
    model="gpt-4o",
    output_type=ExpandedItem,
    hooks=logging_hooks,
)

evaluate_item_agent = Agent(
    name="ItemEvaluator",
    instructions=(
        "You are a STRICT and CRITICAL plan evaluator. Given a goal, a specific success criterion, "
        "a full plan outline, and a detailed expansion of a single plan item, evaluate whether that expanded item, "
        "in the context of the overall plan, adequately addresses the specified success criterion.\n\n"
        
        "Your evaluation must be HIGHLY CRITICAL - always look for weaknesses and gaps in the plan item. "
        "You MUST identify specific strengths AND weaknesses for each evaluation.\n\n"
        
        "Rate the item on a 5-point scale, where:\n"
        "1 = Poor (Fails to address the criterion in any meaningful way)\n"
        "2 = Below Average (Addresses some aspects but has major gaps or issues)\n"
        "3 = Average (Adequately addresses the criterion with some notable weaknesses)\n"
        "4 = Good (Addresses criterion well with minor weaknesses)\n"
        "5 = Excellent (Completely addresses the criterion with no significant weaknesses)\n\n"
        
        "A PASSING item must score at least 3/5. Any item scoring below 3 is a FAIL.\n\n"
        
        "You MUST provide:\n"
        "1. At least two specific strengths of the item\n"
        "2. At least two specific weaknesses of the item (even for high-scoring items)\n"
        "3. Your rating (1-5)\n"
        "4. Detailed justification for your rating\n"
        "5. At least two specific suggestions for improvement\n"
        "6. Final determination: 'pass' or 'fail'\n"
        "7. Comprehensive reasoning for your determination\n\n"
        
        "EXAMPLES OF PROPER EVALUATIONS:\n" +
        PASS_EXAMPLE + "\n" +
        FAIL_EXAMPLE + "\n\n"
        
        "Remember to be CRITICAL in your evaluation. Even good items can be improved. "
        "Do NOT give a high rating unless the item COMPLETELY and EFFECTIVELY addresses the criterion. "
        "When in doubt, err on the side of STRICTNESS."
    ),
    model="gpt-4o",
    output_type=EvalResult,
    hooks=logging_hooks,
)

async def validate_module3_output(
    context: RunContextWrapper[None], agent: Agent, agent_output: Any
) -> GuardrailFunctionOutput:
    """Validates the output of Module 3."""
    try:
        log_info("Validating Module 3 output...")
        # Log only a truncated version of the output to avoid excessive logging
        truncated_output = {k: v for k, v in agent_output.model_dump().items() if k != 'expanded_outline'}
        log_info(f"Output to validate (truncated): {json.dumps(truncated_output, indent=2)}", truncate=True, max_length=5000)
        verbose_logger.info(f"Full output to validate: {json.dumps(agent_output.model_dump(), indent=2)}")
        
        Module3Output.model_validate(agent_output)
        log_info("Module 3 output validation passed")
        return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)
    except ValidationError as e:
        logger.error(f"Module 3 output validation failed: {e}")
        verbose_logger.error(f"Module 3 output validation failed: {e}")
        return GuardrailFunctionOutput(
            output_info={"error": str(e)}, tripwire_triggered=True
        )

async def process_item(
    goal: str,
    success_criteria: list[SuccessCriteria],
    plan_outline: PlanOutline,
    item: PlanItem,
    context: RunContextWrapper[None],
    item_index: int,
) -> tuple[PlanItem, list[EvalResult]]:
    """Expands and evaluates a single plan item against all success criteria."""
    log_info(f"Processing plan item {item_index+1}: {item.item_title}")
    
    # Format all criteria for expansion
    criteria_text = "\n".join([f"- {c.criteria}" for c in success_criteria])
    
    # Expand the item
    log_info(f"Expanding item: {item.item_title}")
    expand_input = (
        f"Goal: {goal}\n"
        f"Success Criteria:\n{criteria_text}\n"
        f"Plan Outline: {plan_outline.plan_title}\n"
        f"Plan Description: {plan_outline.plan_description}\n"
        f"Item to Expand:\nTitle: {item.item_title}\nDescription: {item.item_description}"
    )
    
    log_info(f"Expansion input: {expand_input}", truncate=True, max_length=5000)
    
    expand_result = await Runner.run(
        expand_item_agent,
        input=expand_input,
        context=context,
    )
    expanded_item_text = expand_result.final_output.expanded_text
    
    # Sanitize the text to ensure no corruption
    expanded_item_text = sanitize_text(expanded_item_text)
    log_info(f"Item expanded to {len(expanded_item_text)} characters")

    # Create a new PlanItem with the expanded description
    expanded_item = PlanItem(item_title=item.item_title, item_description=expanded_item_text)
    
    # Evaluate the expanded item against each success criterion
    log_info(f"Evaluating expanded item against {len(success_criteria)} criteria")
    eval_results = []
    
    for i, criterion in enumerate(success_criteria):
        log_info(f"Evaluating against criterion {i+1}: {criterion.criteria}")
        
        # Create evaluation input focusing on this specific criterion
        evaluation_input = (
            f"Goal: {goal}\n\n"
            f"Success Criterion: {criterion.criteria}\n"
            f"Criterion Reasoning: {criterion.reasoning}\n\n"
            f"Plan Outline Title: {plan_outline.plan_title}\n"
            f"Plan Description: {plan_outline.plan_description}\n\n"
            f"Item Title: {item.item_title}\n"
            f"Expanded Item:\n\n{expanded_item_text}\n\n"
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
        
        # Get the result and ensure it has the criterion included
        result = evaluation_result.final_output
        
        # Ensure the criteria field is set correctly
        result_dict = result.model_dump()
        if 'criteria' not in result_dict or not result_dict['criteria']:
            result_dict['criteria'] = criterion.model_dump()
            # Recreate the EvalResult with the updated dictionary
            result = EvalResult.model_validate(result_dict)
        
        # Ensure reasoning text is sanitized
        result.reasoning = sanitize_text(result.reasoning)
        
        eval_results.append(result)
        log_info(f"Evaluation result for criterion {i+1}: {result.result} - Rating: {result.strengths_weaknesses.rating}/5")
        log_info(f"Reasoning: {result.reasoning[:200]}...", truncate=True, max_length=5000)
    
    return expanded_item, eval_results

def generate_criteria_summary(evaluation_results: list[EvalResult]) -> Dict[str, Dict[str, int]]:
    """Generate a summary of how items performed against each criterion."""
    summary = {}
    
    # Group evaluation results by criterion
    for result in evaluation_results:
        criterion = result.criteria.criteria
        if criterion not in summary:
            summary[criterion] = {"pass": 0, "fail": 0, "total": 0, "avg_rating": 0, "ratings": []}
        
        summary[criterion][result.result] += 1
        summary[criterion]["total"] += 1
        summary[criterion]["ratings"].append(result.strengths_weaknesses.rating)
    
    # Calculate average ratings
    for criterion, data in summary.items():
        if data["ratings"]:
            data["avg_rating"] = sum(data["ratings"]) / len(data["ratings"])
            # Remove the ratings list from the final summary
            del data["ratings"]
    
    return summary

async def run_module_3(input_file: str, output_file: str) -> None:
    """Runs Module 3."""
    context = RunContextWrapper(context=None)

    try:
        log_info(f"Starting Module 3, reading input from {input_file}")
        with open(input_file, "r") as f:
            module_2_data = json.load(f)
            log_info(f"Successfully loaded data from {input_file}")

        # Convert to Pydantic objects
        module_2_output = Module2Output.model_validate(module_2_data)
        goal = module_2_output.goal
        selected_criteria = module_2_output.selected_criteria
        selected_plan = module_2_output.selected_outline
        
        log_info(f"Goal: {goal}")
        log_info(f"Number of selected criteria: {len(selected_criteria)}")
        for i, criterion in enumerate(selected_criteria):
            log_info(f"Criterion {i+1}: {criterion.criteria}")
        log_info(f"Selected plan: {selected_plan.plan_title}")
        log_info(f"Number of plan items: {len(selected_plan.plan_items)}")

        # Process each plan item sequentially
        # (Using sequential processing to ensure consistent and stable output)
        log_info("Processing all plan items...")
        expanded_plan_items = []
        all_eval_results = []
        
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
            all_eval_results.extend(item_eval_results)
            
            log_info(f"Completed processing item {i+1}: {item.item_title}")
            
            # Log pass/fail count for this item
            pass_count = sum(1 for r in item_eval_results if r.result == "pass")
            fail_count = sum(1 for r in item_eval_results if r.result == "fail")
            log_info(f"Item {i+1} results: {pass_count} pass, {fail_count} fail")

        # Create a new plan outline with the expanded items
        log_info("Creating expanded outline with expanded items")
        expanded_outline = PlanOutline(
            plan_title=selected_plan.plan_title,
            plan_description=selected_plan.plan_description,
            plan_items=expanded_plan_items,
            reasoning=selected_plan.reasoning,
            rating=selected_plan.rating,
            created_by=selected_plan.created_by
        )
        
        # Generate criteria summary
        criteria_summary = generate_criteria_summary(all_eval_results)
        log_info(f"Criteria summary: {json.dumps(criteria_summary, indent=2)}")

        # Create the output object
        log_info("Creating Module 3 output object")
        module_3_output = Module3Output(
            goal=goal,
            selected_criteria=selected_criteria,
            selected_outline=selected_plan,     # Original outline
            expanded_outline=expanded_outline,  # Expanded outline
            evaluation_results=all_eval_results,    # All evaluation results
            criteria_summary=criteria_summary,      # Summary of results
        )

        # Apply guardrail
        log_info("Applying output guardrail...")
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
        
        log_info(f"Module 3 completed. Output saved to {output_file}")
        log_info(f"Timestamped output saved to {timestamped_file}")

    except Exception as e:
        logger.error(f"An error occurred in Module 3: {e}")
        verbose_logger.error(f"An error occurred in Module 3: {e}")
        import traceback
        error_trace = traceback.format_exc()
        logger.error(error_trace)
        verbose_logger.error(error_trace)  # Log the full stack trace

async def main():
    log_info("Starting main function")
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    input_file = os.path.join(input_dir, "module2_output.json")
    output_file = os.path.join(input_dir, "module3_output.json")
    await run_module_3(input_file, output_file)
    log_info("Main function completed")

if __name__ == "__main__":
    log_info("Module 3 script starting")
    asyncio.run(main())
    log_info("Module 3 script completed")
You (the entity reading this content) are a large language model by OpenAI.  You are powering an application called "Codex".  Below is the context from OpenAI about what Codex (you) are.  I am sharing this information with you for your awareness and so you can be the best CodeX you can be.


__________

Codex
=====

Delegate tasks to a software engineering agent in the cloud.

Codex is a cloud-based software engineering agent. Use it to fix bugs, review code, do refactors, and fix pieces of code in response to user feedback. It's powered by a version of [OpenAI o3](/docs/models/o3) that's fine-tuned for real-world software development.

Overview
--------

We believe in a future where developers drive the work they want to own, delegating toilsome tasks to agents. We see early signs of this future today at OpenAI, with Codex working in its own environment and drafting pull requests in our repos.

**Codex vs. Codex CLI**  
These docs cover Codex, a cloud-based agent you can find in your browser. For an open-source CLI agent you can run locally in your terminal, [install Codex CLI](https://github.com/openai/codex#openai-codex-cli).

Connect your GitHub
-------------------

To grant the Codex agent access to your GitHub repos, install our GitHub app to your organization. The two permissions required are ability to _clone the repo_ and the ability to _push a pull request_ to it. Our app **will not write to your repo without your permission**.

Each user in your organization must authenticate with their GitHub account before being able to use Codex. After auth, we grant access to your GitHub repos and environments at the ChatGPT workspace level—meaning if your teammate grants access to a repo, you'll also be able to run Codex tasks in that repo, as long as you share a [workspace](https://help.openai.com/en/articles/8798594-what-is-a-workspace-how-do-i-access-my-chatgpt-team-workspace).

### How it works

At a high level, you specify a prompt, and the agent goes to work in its own environment. After about 8–10 minutes, the agent gives you back a diff.

You can execute prompts in either _ask_ mode or _code_ mode. When you select _ask_, Codex clones a read-only version of your repo, booting faster and giving you follow-up tasks. _Code_ mode, however, creates a full-fledged environment that the agent can run and test against.

Exact flow:

1.  You navigate to [chatgpt.com/codex](http://chatgpt.com/codex) and **submit a task**.
2.  We launch a new **Docker container** based upon our [**base image**](https://github.com/openai/codex-universal). We then **clone your repo** at the desired **branch or sha** and run any **setup scripts** you have from the specified **workdir**.
3.  We **disable network access**. The agent does not have the ability to install dependencies from this point forward.
4.  The agent then **runs terminal commands in a loop**. It writes code, runs tests, and attempts to check its work. The agent attempts to honor any specified lint or test commands you've defined in an `AGENTS.md` file. The agent does not have access to any special tools outside of the terminal or CLI tools you provide.
5.  When the agent completes your task, it **presents a a diff** or a set of follow-up tasks. You can choose to **open a PR** or respond with follow-up comments to ask for additional changes.

Submit tasks to Codex
---------------------

After connecting your repository, begin sending tasks using one of two modes:

*   **Ask mode** for brainstorming, audits, or architecture questions
*   **Code mode** for when you want automated refactors, tests, or fixes applied

Below are some example tasks to get you started with Codex.

### Ask mode examples

Use ask mode to get advice and insights on your code, no changes applied.

*   **Refactoring suggestions**
    
    Codex can help brainstorm structural improvements, such as splitting files, extracting functions, and tightening documentation.
    
    ```text
    Take a look at <hairiest file in my codebase>.
    Can you suggest better ways to split it up, test it, and isolate functionality?
    ```
    
*   **Q&A and architecture understanding**
    
    Codex can answer deep questions about your codebase and generate diagrams.
    
    ```text
    Document and create a mermaidjs diagram of the full request flow from the client 
    endpoint to the database.
    ```
    

### Code mode examples

Use code mode when you want Codex to actively modify code and prepare a pull request.

*   **Security vulnerabilities**
    
    Codex excels at auditing intricate logic and uncovering security flaws.
    
    ```text
    There's a memory-safety vulnerability in <my package>. Find it and fix it.
    ```
    
*   **Code review**
    
    Append `.diff` to any pull request URL and include it in your prompt. Codex loads the patch inside the container.
    
    ```text
    Please review my code and suggest improvements. The diff is below:
    <diff>
    ```
    
*   **Adding tests**
    
    After implementing initial changes, follow up with targeted test generation.
    
    ```text
    From my branch, please add tests for the following files:
    <files>
    ```
    
*   **Bug fixing**
    
    A stack trace is usually enough for Codex to locate and correct the problem.
    
    ```text
    Find and fix a bug in <my package>.
    ```
    
*   **Product and UI fixes**
    
    Although Codex cannot render a browser, it can resolve minor UI regressions.
    
    ```text
    The modal on our onboarding page isn't centered. Can you fix it?
    ```
    

Advanced configuration
----------------------

Codex works out of the box, but you can point it at a custom environment to have the agent install dependencies, compile, lint, test, or spin up services exactly the way your project needs.

### Create an environment

By default, the agent runs in a Docker container running our universal image. It comes pre-installed with most popular languages (Python, Go, Rust, Java, Ruby). See the [base Dockerfile](https://github.com/openai/codex-universal).

### Add setup commands

After the repo is cloned to the `/workspace` directory, we run all the specified setup commands.

To get the best results from the agent, make sure you install dependencies (public and private), lint frameworks, and everything required to run unit tests. Specify setup commands—either multiple commands per line or one per line—and add the setup file to your repo.

### Create an AGENTS.md

Provide common context by adding an `AGENTS.md` file. This is just a standard Markdown file the agent reads to understand how to work in your repository. `AGENTS.md` can be nested, and the agent will by default respect whatever the most nested root that it's looking for. Some customers also prompt the agent to look for `.currsorrules` or `CLAUDE.md` explicitly. We recommend sharing any bits of organization-wide configuration in this file.

Common things you might want to include:

*   An overview showing which particular files and folders to work in
*   Contribution and style guidelines
*   Parts of the codebase being migrated
*   How to validate changes (running lint, tests, etc.)

Here's an example as one way to structure your `AGENTS.md` file:

AGENTS.md

```markdown
# Contributor Guide

## Dev Environment Tips
- Use pnpm dlx turbo run where <project_name> to jump to a package instead of scanning with ls.
- Run pnpm install --filter <project_name> to add the package to your workspace so Vite, ESLint, and TypeScript can see it.
- Use pnpm create vite@latest <project_name> -- --template react-ts to spin up a new React + Vite package with TypeScript checks ready.
- Check the name field inside each package's package.json to confirm the right name—skip the top-level one.

## Testing Instructions
- Find the CI plan in the .github/workflows folder.
- Run pnpm turbo run test --filter <project_name> to run every check defined for that package.
- From the package root you can just call pnpm test. The commit should pass all tests before you merge.
- To focus on one step, add the Vitest pattern: pnpm vitest run -t "<test name>".
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run pnpm lint --filter <project_name> to be sure ESLint and TypeScript rules still pass.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
Title format: [<project_name>] <Title>
```

Prompting tips
--------------

Just like ChatGPT, Codex is only as effective as the instructions you give it. Use the following tips.

*   **Use greppable names**. Codex literally calls `grep`, so specific filenames, symbols, or unique package names help it quickly find the right spot. Internally, we use the prefix `wham` for Codex-related packages.
*   **Tell it where to work**. Codex performs best when pointed at a single file or at most a package containing ~100 files. Broad or vague prompts can leave the agent guessing.
*   **Paste the full stack trace**. Exact stack traces with file paths and line numbers help Codex immediately pinpoint bugs.
*   **Spin up multiple tasks in a row**. Each task runs in its own isolated environment, so feel free to queue multiple tasks simultaneously. Many engineers at OpenAI start their day by making a quick to-do list and firing off several tasks at once.
*   **Give it work with a pass/fail**. Just like a human, Codex validates its changes. Since it has access to a terminal, anything verifiable with a unit test or linting lands more reliably. (Codex doesn't yet support UI tests.)
*   **Split large changes**. Instead of giving Codex a giant PR, break work into small, focused tasks. Smaller tasks are easier for the agent to test individually and easier for you to review.
*   **Let Codex take over when you're stuck**. If you get blocked, create a branch and hand the problem to Codex. You can use this strategy to explore multiple solutions in parallel.
*   **Kick off a few tasks before you start your day**. Launch tasks before your commute or morning coffee, and come back to fresh diffs ready for review.

Was this page useful?

// convex/agent.ts
"use node";

import { Agent } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { sandbox_read_directory, sandbox_read_file, sandbox_read_status, sandbox_write_file } from "./tools";

function createAgent() {
  return new Agent<{sandboxId: string}>(components.agent, {
    name: "Designer Agent",
    languageModel: "anthropic/claude-sonnet-4.5",
    instructions: "You are an app ui designer agent.",
    tools: {
        sandbox_read_directory,
        sandbox_read_status,
        sandbox_write_file,
        sandbox_read_file,
    },
    maxSteps: 5,
  });
}

export { createAgent };

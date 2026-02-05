"use node";

import { v } from "convex/values";
import { action } from "./_generated/server";
import { createAgent } from "./agent";

const sendMessageToAgent = action({
  args: {
    threadId: v.string(),
    prompt: v.string(),
    sandboxId: v.string(),
  },
  handler: async (ctx, { prompt, threadId, sandboxId }) => {
    const agent = createAgent();
    const { thread } = await agent.continueThread({...ctx, sandboxId}, {
      threadId: threadId,
    });
    const result = await thread.generateText({ prompt } as any);
    console.log("Result: ", result.text);
    return result.text;
  },
});


const DEMO_ID = "test-123";

const createThread = action({
  args: {},
  handler: async (ctx) => {
    const agent = createAgent();
    const { threadId } = await agent.createThread(ctx, {
      userId: DEMO_ID,
    });
    return threadId;
  },
});

export { sendMessageToAgent, createThread };
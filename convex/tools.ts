"use node";

import { createTool, ToolCtx } from "@convex-dev/agent";
import { Sandbox } from '@vercel/sandbox';
import { z } from "zod";

type MyCtx = ToolCtx & { sandboxId: string };

export const sandbox_read_status = createTool({
    description: "Fetch sandbox status.",
    args: z.object({}),
    handler: async (ctx: MyCtx, args) => {
        const sandboxId = ctx.sandboxId
        if (!sandboxId) throw new Error("sandboxId required");

        const sandbox = await Sandbox.get({ sandboxId: sandboxId });

        return { status: sandbox.status };
    },
})

export const sandbox_read_directory = createTool({
    description: "List files in directory",
    args: z.object({
        path: z.string().describe("Path to the folder inside the sandbox")
    }),
    handler: async (ctx: MyCtx, args) => {
        const sandboxId = ctx.sandboxId
        if (!sandboxId) throw new Error("sandboxId required");

        const sandbox = await Sandbox.get({ sandboxId: sandboxId });
        const result = await sandbox.runCommand("ls", [`"${args.path}"`])
        
        return { output: result.stdout(), error: result.stderr() };
    },
})

export const sandbox_read_file = createTool({
    description: "Read file contents",
    args: z.object({
        path: z.string().describe("Path to the file inside the sandbox"),
    }),
    handler: async (ctx: MyCtx, args) => {
        const sandboxId = ctx.sandboxId
        if (!sandboxId) throw new Error("sandboxId required");

        const sandbox = await Sandbox.get({ sandboxId: sandboxId });

        const stream = await sandbox.readFile({path: args.path})

        if (!stream) throw new Error("Stream is null")

        return {output: stream.read()}
    },
})

export const sandbox_write_file = createTool({
    description: "Write file contents",
    args: z.object({
        path: z.string().describe("Path to the file inside the sandbox"),
        content: z.string().describe("File contents to write")
    }),
    handler: async (ctx: MyCtx, args) => {
        const sandboxId = ctx.sandboxId
        if (!sandboxId) throw new Error("sandboxId required");

        const sandbox = await Sandbox.get({ sandboxId: sandboxId });
        await sandbox.writeFiles([{ path: args.path, content: Buffer.from(args.content)}]);
    },
})
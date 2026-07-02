import { readFile } from 'node:fs/promises'
import { z } from 'zod'

const configSchema = z.object({
  port: z.number().int().min(1).max(65535),
  logLevel: z.enum(['debug', 'info', 'warn', 'error']),
  database: z.object({
    host: z.string().min(1),
    port: z.number().int().min(1).max(65535),
    name: z.string().min(1),
  }),
})

export type AppConfig = z.infer<typeof configSchema>

export async function loadConfig(path: string): Promise<AppConfig> {
  const raw = await readFile(path, 'utf-8')
  const parsed: unknown = JSON.parse(raw)
  const result = configSchema.safeParse(parsed)
  if (!result.success) {
    throw new Error(`Invalid config at ${path}: ${result.error.message}`)
  }
  return result.data
}

export function overrideFromEnv(config: AppConfig, env: NodeJS.ProcessEnv): AppConfig {
  const port = env.APP_PORT ? Number(env.APP_PORT) : config.port
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error(`APP_PORT must be a valid port number, got: ${env.APP_PORT}`)
  }
  return { ...config, port }
}

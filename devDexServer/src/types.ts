export type Protocol = "http" | "https"

export type Config = {
    port: string,
    hostname: string,
    protocol: Protocol,
    projectName: string,
    token: string,
    version: string,
}
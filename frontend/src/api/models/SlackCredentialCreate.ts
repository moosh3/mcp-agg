/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Schema for creating Slack credentials
 */
export type SlackCredentialCreate = {
    token_type?: string;
    scope?: (string | null);
    team_id?: (string | null);
    team_name?: (string | null);
    access_token: string;
};


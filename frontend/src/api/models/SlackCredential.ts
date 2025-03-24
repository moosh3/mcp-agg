/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Schema for Slack credential responses
 */
export type SlackCredential = {
    token_type?: string;
    scope?: (string | null);
    team_id?: (string | null);
    team_name?: (string | null);
    id: number;
    user_id: number;
    access_token: string;
    created_at: string;
    updated_at?: (string | null);
};


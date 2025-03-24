/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { App } from './App';
export type User = {
    email: string;
    id: number;
    is_active: boolean;
    is_admin: boolean;
    created_at: string;
    updated_at?: (string | null);
    apps?: Array<App>;
};


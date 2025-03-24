/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_api_v1_token_post } from '../models/Body_login_api_v1_token_post';
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthenticationService {
    /**
     * Register User
     * Register a new user.
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static registerUserApiV1RegisterPost(
        requestBody: UserCreate,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Login
     * Login to get access token.
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginApiV1TokenPost(
        formData: Body_login_api_v1_token_post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Read Users Me
     * Get current user information.
     * @returns User Successful Response
     * @throws ApiError
     */
    public static readUsersMeApiV1MeGet(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/me',
        });
    }
    /**
     * Check Auth
     * Check if user is authenticated.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static checkAuthApiV1CheckGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/check',
        });
    }
    /**
     * List Accounts
     * List all user accounts (admin only).
     * @param skip
     * @param limit
     * @returns any Successful Response
     * @throws ApiError
     */
    public static listAccountsApiV1AccountsGet(
        skip?: number,
        limit: number = 100,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/accounts',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update User Status
     * Update user status (admin only).
     * @param userId
     * @param isActive
     * @param isAdmin
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateUserStatusApiV1UsersUserIdPatch(
        userId: number,
        isActive?: (boolean | null),
        isAdmin?: (boolean | null),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            query: {
                'is_active': isActive,
                'is_admin': isAdmin,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete User
     * Delete a user (admin only).
     * @param userId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteUserApiV1UsersUserIdDelete(
        userId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}

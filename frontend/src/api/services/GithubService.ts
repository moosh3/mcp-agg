/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GitHubCredential } from '../models/GitHubCredential';
import type { GitHubCredentialCreate } from '../models/GitHubCredentialCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class GithubService {
    /**
     * Connect Github
     * Connect GitHub account by providing an OAuth access token.
     *
     * Args:
     * credentials (GitHubCredentialCreate): GitHub credentials
     * db (Session): Database session
     * current_user (User): Current authenticated user
     *
     * Returns:
     * GitHubCredentialSchema: Saved GitHub credentials
     * @param requestBody
     * @returns GitHubCredential Successful Response
     * @throws ApiError
     */
    public static connectGithubApiV1AppsGithubConnectPost(
        requestBody: GitHubCredentialCreate,
    ): CancelablePromise<GitHubCredential> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/apps/github/connect',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Repositories
     * List repositories for the authenticated GitHub user.
     *
     * Args:
     * github_client (GitHubClient): Authenticated GitHub client
     *
     * Returns:
     * Dict[str, Any]: List of repositories
     * @returns any Successful Response
     * @throws ApiError
     */
    public static listRepositoriesApiV1AppsGithubRepositoriesGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/github/repositories',
            errors: {
                404: `Not found`,
            },
        });
    }
    /**
     * Get User
     * Get authenticated GitHub user information.
     *
     * Args:
     * github_client (GitHubClient): Authenticated GitHub client
     *
     * Returns:
     * Dict[str, Any]: User information
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUserApiV1AppsGithubUserGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/github/user',
            errors: {
                404: `Not found`,
            },
        });
    }
    /**
     * List Issues
     * List issues for a GitHub repository.
     *
     * Args:
     * owner (str): Repository owner
     * repo (str): Repository name
     * github_client (GitHubClient): Authenticated GitHub client
     *
     * Returns:
     * Dict[str, Any]: List of issues
     * @param owner
     * @param repo
     * @returns any Successful Response
     * @throws ApiError
     */
    public static listIssuesApiV1AppsGithubRepositoriesOwnerRepoIssuesGet(
        owner: string,
        repo: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/github/repositories/{owner}/{repo}/issues',
            path: {
                'owner': owner,
                'repo': repo,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Issue
     * Create a new issue in a GitHub repository.
     *
     * Args:
     * owner (str): Repository owner
     * repo (str): Repository name
     * title (str): Issue title
     * body (str, optional): Issue body. Defaults to None.
     * github_client (GitHubClient): Authenticated GitHub client
     *
     * Returns:
     * Dict[str, Any]: Created issue information
     * @param owner
     * @param repo
     * @param title
     * @param body
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createIssueApiV1AppsGithubRepositoriesOwnerRepoIssuesPost(
        owner: string,
        repo: string,
        title: string,
        body?: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/apps/github/repositories/{owner}/{repo}/issues',
            path: {
                'owner': owner,
                'repo': repo,
            },
            query: {
                'title': title,
                'body': body,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
}

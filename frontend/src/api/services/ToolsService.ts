/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExecuteToolRequest } from '../models/ExecuteToolRequest';
import type { ExecuteToolResponse } from '../models/ExecuteToolResponse';
import type { MCPUrlResponse } from '../models/MCPUrlResponse';
import type { Tool } from '../models/Tool';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ToolsService {
    /**
     * List App Tools
     * List all tools available for a specific app
     *
     * Args:
     * app (str): App name (e.g., 'github')
     * db (Session): Database session
     *
     * Returns:
     * List[schemas.Tool]: List of tools for the app
     * @param app
     * @returns Tool Successful Response
     * @throws ApiError
     */
    public static listAppToolsApiV1AppsAppToolsGet(
        app: string,
    ): CancelablePromise<Array<Tool>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/{app}/tools/',
            path: {
                'app': app,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Tool
     * Get a specific tool by app and tool name
     *
     * Args:
     * app (str): App name (e.g., 'github')
     * tool (str): Tool name (e.g., 'github.list_repos')
     * db (Session): Database session
     *
     * Returns:
     * schemas.Tool: Tool details
     *
     * Raises:
     * HTTPException: If tool is not found
     * @param app
     * @param tool
     * @returns Tool Successful Response
     * @throws ApiError
     */
    public static getToolApiV1AppsAppToolsToolGet(
        app: string,
        tool: string,
    ): CancelablePromise<Tool> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/{app}/tools/{tool}/',
            path: {
                'app': app,
                'tool': tool,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Guess Tools
     * @param description
     * @returns any Successful Response
     * @throws ApiError
     */
    public static guessToolsApiV1GuessToolsGet(
        description: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/guess-tools/',
            query: {
                'description': description,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Execute Tool
     * Execute a tool with provided parameters
     *
     * Args:
     * request (schemas.ExecuteToolRequest): Tool execution request
     * db (Session): Database session
     * current_user (models.User): Current authenticated user
     *
     * Returns:
     * schemas.ExecuteToolResponse: Execution result
     *
     * Raises:
     * HTTPException: If tool is not found or execution fails
     * @param requestBody
     * @returns ExecuteToolResponse Successful Response
     * @throws ApiError
     */
    public static executeToolApiV1ExecutePost(
        requestBody: ExecuteToolRequest,
    ): CancelablePromise<ExecuteToolResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/execute/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Execute Specific Tool
     * Execute a tool by its ID
     *
     * Args:
     * tool_id (int): Tool ID in the database
     * db (Session): Database session
     * current_user (models.User): Current authenticated user
     *
     * Returns:
     * schemas.ExecuteToolResponse: Execution result
     * @param toolId
     * @returns ExecuteToolResponse Successful Response
     * @throws ApiError
     */
    public static executeSpecificToolApiV1ToolsToolIdExecutePost(
        toolId: number,
    ): CancelablePromise<ExecuteToolResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/tools/{tool_id}/execute/',
            path: {
                'tool_id': toolId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Rate Execution
     * @param executionLogId
     * @param rating
     * @returns any Successful Response
     * @throws ApiError
     */
    public static rateExecutionApiV1ExecuteLogExecutionLogIdRatePost(
        executionLogId: number,
        rating: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/execute/log/{execution_log_id}/rate/',
            path: {
                'execution_log_id': executionLogId,
            },
            query: {
                'rating': rating,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Tools
     * @returns Tool Successful Response
     * @throws ApiError
     */
    public static listToolsApiV1ToolsGet(): CancelablePromise<Array<Tool>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tools/',
        });
    }
    /**
     * Generate Mcp Url
     * Generate a unique URL for the user to connect their MCP client
     *
     * This URL contains authentication information that allows the MCP client
     * to access all tools available to the user without additional authentication.
     *
     * Args:
     * db (Session): Database session
     * current_user (models.User): Current authenticated user
     *
     * Returns:
     * schemas.MCPUrlResponse: MCP URL and associated metadata
     * @returns MCPUrlResponse Successful Response
     * @throws ApiError
     */
    public static generateMcpUrlApiV1McpUrlGet(): CancelablePromise<MCPUrlResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/mcp-url/',
        });
    }
    /**
     * Get Tool By Id
     * @param toolId
     * @returns Tool Successful Response
     * @throws ApiError
     */
    public static getToolByIdApiV1ToolsToolIdGet(
        toolId: number,
    ): CancelablePromise<Tool> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tools/{tool_id}/',
            path: {
                'tool_id': toolId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}

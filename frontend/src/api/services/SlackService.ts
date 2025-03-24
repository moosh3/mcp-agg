/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SlackCredential } from '../models/SlackCredential';
import type { SlackCredentialCreate } from '../models/SlackCredentialCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SlackService {
    /**
     * Connect Slack
     * Connect Slack account by providing an OAuth access token.
     *
     * Args:
     * credentials (SlackCredentialCreate): Slack credentials
     * db (Session): Database session
     * current_user (User): Current authenticated user
     *
     * Returns:
     * SlackCredentialSchema: Saved Slack credentials
     * @param requestBody
     * @returns SlackCredential Successful Response
     * @throws ApiError
     */
    public static connectSlackApiV1AppsSlackConnectPost(
        requestBody: SlackCredentialCreate,
    ): CancelablePromise<SlackCredential> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/apps/slack/connect',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Channels
     * List channels for the authenticated Slack workspace.
     *
     * Args:
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: List of channels
     * @returns any Successful Response
     * @throws ApiError
     */
    public static listChannelsApiV1AppsSlackChannelsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/slack/channels',
            errors: {
                404: `Not found`,
            },
        });
    }
    /**
     * Post Message
     * Post a message to a channel.
     *
     * Args:
     * channel_id (str): Channel ID
     * text (str): Message text
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: Message posting result
     * @param channelId
     * @param text
     * @returns any Successful Response
     * @throws ApiError
     */
    public static postMessageApiV1AppsSlackChannelsChannelIdMessagesPost(
        channelId: string,
        text: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/apps/slack/channels/{channel_id}/messages',
            path: {
                'channel_id': channelId,
            },
            query: {
                'text': text,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reply To Thread
     * Reply to a message thread.
     *
     * Args:
     * channel_id (str): Channel ID
     * thread_ts (str): Thread timestamp
     * text (str): Reply text
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: Reply result
     * @param channelId
     * @param threadTs
     * @param text
     * @returns any Successful Response
     * @throws ApiError
     */
    public static replyToThreadApiV1AppsSlackChannelsChannelIdThreadsThreadTsRepliesPost(
        channelId: string,
        threadTs: string,
        text: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/apps/slack/channels/{channel_id}/threads/{thread_ts}/replies',
            path: {
                'channel_id': channelId,
                'thread_ts': threadTs,
            },
            query: {
                'text': text,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Thread Replies
     * Get replies in a thread.
     *
     * Args:
     * channel_id (str): Channel ID
     * thread_ts (str): Thread timestamp
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: Thread replies
     * @param channelId
     * @param threadTs
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getThreadRepliesApiV1AppsSlackChannelsChannelIdThreadsThreadTsRepliesGet(
        channelId: string,
        threadTs: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/slack/channels/{channel_id}/threads/{thread_ts}/replies',
            path: {
                'channel_id': channelId,
                'thread_ts': threadTs,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Channel History
     * Get channel message history.
     *
     * Args:
     * channel_id (str): Channel ID
     * limit (int, optional): Number of messages. Defaults to 10.
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: Channel history
     * @param channelId
     * @param limit
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getChannelHistoryApiV1AppsSlackChannelsChannelIdHistoryGet(
        channelId: string,
        limit: number = 10,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/slack/channels/{channel_id}/history',
            path: {
                'channel_id': channelId,
            },
            query: {
                'limit': limit,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Users
     * List users in the Slack workspace.
     *
     * Args:
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: List of users
     * @returns any Successful Response
     * @throws ApiError
     */
    public static listUsersApiV1AppsSlackUsersGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/slack/users',
            errors: {
                404: `Not found`,
            },
        });
    }
    /**
     * Get User Profile
     * Get user profile.
     *
     * Args:
     * user_id (str): User ID
     * slack_client (SlackClient): Authenticated Slack client
     *
     * Returns:
     * Dict[str, Any]: User profile
     * @param userId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUserProfileApiV1AppsSlackUsersUserIdGet(
        userId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/apps/slack/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }
}

/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class HealthService {
    /**
     * Liveness
     * @returns any Successful Response
     * @throws ApiError
     */
    public static livenessApiV1ApiV1HealthLivenessGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/api/v1/health/liveness',
        });
    }
    /**
     * Readiness
     * @returns any Successful Response
     * @throws ApiError
     */
    public static readinessApiV1ApiV1HealthReadinessGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/api/v1/health/readiness',
        });
    }
    /**
     * Metrics
     * @returns any Successful Response
     * @throws ApiError
     */
    public static metricsApiV1ApiV1HealthMetricsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/api/v1/health/metrics',
        });
    }
}

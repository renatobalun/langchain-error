# config.py
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhook/error")
ERROR_ROTATION_INTERVAL = int(os.getenv("ERROR_ROTATION_INTERVAL", "60"))  # seconds

ERRORS = [
    {
        "name": "DatabaseConnectionError",
        "status_code": 503,
        "detail": "Unable to connect to database. Connection pool exhausted.",
        "severity": "error",
        "context": {
            "service": "user-service",
            "database": "PostgreSQL",
            "host": "db.production.internal",
            "port": 5432,
            "connection_pool_size": 10,
            "active_connections": 10,
            "error_message": "FATAL: remaining connection slots are reserved for non-replication superuser connections",
            "stack_trace": """
  File "/app/services/user_service.py", line 45, in get_user
    connection = pool.get_connection()
  File "/app/db/pool.py", line 23, in get_connection
    raise DatabaseConnectionError("Connection pool exhausted")
            """.strip(),
            "environment": "production",
            "pod_name": "user-service-7d8f9c-xyz",
            "namespace": "backend",
            "attempted_retries": 3,
            "last_successful_connection": "2024-01-15T10:30:00Z"
        },
        "metrics": {
            "cpu_usage": "85%",
            "memory_usage": "92%",
            "request_rate": "450 req/sec",
            "avg_response_time": "2.5s",
            "error_rate": "15%"
        },
        "suggested_checks": [
            "Check database connection pool configuration",
            "Verify database server is running and accessible",
            "Check for connection leaks in application code",
            "Review max_connections setting in PostgreSQL",
            "Check if there are long-running queries blocking connections"
        ]
    },
    {
        "name": "AuthenticationError",
        "status_code": 401,
        "detail": "Invalid authentication credentials. Token has expired.",
        "severity": "warning",
        "context": {
            "service": "auth-service",
            "user_id": "user_7d89f3a1",
            "token_type": "JWT",
            "token_issued_at": "2024-01-15T08:00:00Z",
            "token_expired_at": "2024-01-15T09:00:00Z",
            "endpoint": "/api/v1/users/profile",
            "ip_address": "192.168.1.105",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "stack_trace": """
  File "/app/middleware/auth.py", line 67, in verify_token
    decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
  File "/usr/local/lib/python3.11/site-packages/jwt/api_jwt.py", line 120, in decode
    raise ExpiredSignatureError('Signature has expired')
            """.strip(),
            "auth_provider": "internal",
            "last_successful_login": "2024-01-15T07:55:00Z",
            "failed_attempts_today": 2
        },
        "metrics": {
            "active_sessions": 1234,
            "token_refresh_rate": "120 req/min",
            "failed_auth_attempts_last_hour": 45,
            "avg_token_lifetime": "3600s"
        },
        "suggested_checks": [
            "Implement automatic token refresh mechanism",
            "Check token expiration time configuration",
            "Verify client-side token storage and renewal logic",
            "Check system time synchronization across services",
            "Review session management implementation"
        ]
    },
    {
        "name": "RateLimitError",
        "status_code": 429,
        "detail": "Rate limit exceeded. Too many requests from this IP address.",
        "severity": "warning",
        "context": {
            "service": "api-gateway",
            "ip_address": "203.0.113.45",
            "user_id": "user_9f2a1c8d",
            "endpoint": "/api/v1/search",
            "rate_limit_config": {
                "max_requests": 100,
                "time_window": "60 seconds",
                "current_count": 156
            },
            "window_start": "2024-01-15T10:44:00Z",
            "window_end": "2024-01-15T10:45:00Z",
            "stack_trace": """
  File "/app/middleware/rate_limiter.py", line 34, in check_rate_limit
    if request_count > limit:
  File "/app/middleware/rate_limiter.py", line 35, in check_rate_limit
    raise RateLimitExceeded(f"Rate limit of {limit} exceeded")
            """.strip(),
            "client_type": "mobile_app",
            "api_key": "ak_prod_7d8f9c2a",
            "previous_violations": 3,
            "account_tier": "free"
        },
        "metrics": {
            "total_requests_last_minute": 156,
            "unique_ips_blocked_last_hour": 23,
            "avg_requests_per_user": 45,
            "peak_request_time": "10:30-11:00 UTC"
        },
        "suggested_checks": [
            "Review rate limit configuration for different user tiers",
            "Implement exponential backoff in client application",
            "Check for potential bot or scraper activity",
            "Consider implementing request queuing",
            "Review if rate limits are appropriate for use case"
        ]
    },
    {
        "name": "ValidationError",
        "status_code": 422,
        "detail": "Request validation failed. Missing required field 'user_id'.",
        "severity": "warning",
        "context": {
            "service": "order-service",
            "endpoint": "/api/v1/orders/create",
            "http_method": "POST",
            "request_body": {
                "order_items": [
                    {"product_id": "prod_123", "quantity": 2}
                ],
                "shipping_address": "123 Main St",
                "total_amount": 99.99
            },
            "validation_errors": [
                {
                    "field": "user_id",
                    "error": "Field required",
                    "type": "missing"
                }
            ],
            "stack_trace": """
  File "/app/routers/orders.py", line 78, in create_order
    validated_data = OrderCreateSchema(**request_data)
  File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 341, in __init__
    raise ValidationError(errors, self.__class__)
            """.strip(),
            "schema_version": "v1.2.0",
            "client_version": "mobile_app_v2.1.0",
            "request_id": "req_7d8f9c2a1b3e"
        },
        "metrics": {
            "validation_errors_last_hour": 34,
            "most_common_missing_field": "user_id",
            "client_version_distribution": {
                "v2.1.0": "45%",
                "v2.0.0": "35%",
                "v1.9.0": "20%"
            }
        },
        "suggested_checks": [
            "Update API documentation with required fields",
            "Add better error messages in client application",
            "Implement request validation on client side",
            "Check if schema changes were properly communicated",
            "Review API versioning strategy"
        ]
    },
    {
        "name": "ExternalAPIError",
        "status_code": 502,
        "detail": "External payment gateway service is unavailable.",
        "severity": "error",
        "context": {
            "service": "payment-service",
            "external_service": "Stripe API",
            "endpoint_called": "https://api.stripe.com/v1/payment_intents",
            "http_method": "POST",
            "timeout_duration": "30 seconds",
            "error_response": {
                "status_code": 503,
                "body": "Service Temporarily Unavailable",
                "headers": {
                    "Retry-After": "120"
                }
            },
            "stack_trace": """
  File "/app/services/payment_service.py", line 123, in process_payment
    response = requests.post(stripe_url, data=payload, timeout=30)
  File "/usr/local/lib/python3.11/site-packages/requests/api.py", line 115, in post
    return request('post', url, data=data, **kwargs)
  File "/app/services/payment_service.py", line 125, in process_payment
    raise ExternalAPIError("Stripe API unavailable")
            """.strip(),
            "transaction_id": "txn_7d8f9c2a",
            "amount": 149.99,
            "currency": "USD",
            "retry_count": 2,
            "circuit_breaker_state": "half-open",
            "last_successful_call": "2024-01-15T10:40:00Z"
        },
        "metrics": {
            "external_api_uptime": "99.2%",
            "avg_response_time": "450ms",
            "failed_calls_last_hour": 12,
            "circuit_breaker_trips_today": 3,
            "pending_transactions": 23
        },
        "suggested_checks": [
            "Check external service status page",
            "Implement circuit breaker pattern",
            "Add request retry logic with exponential backoff",
            "Consider implementing fallback payment provider",
            "Review timeout configurations",
            "Implement queuing for failed transactions"
        ]
    },
    {
        "name": "ResourceNotFoundError",
        "status_code": 404,
        "detail": "The requested resource with ID '12345' was not found in the system.",
        "severity": "info",
        "context": {
            "service": "inventory-service",
            "resource_type": "Product",
            "resource_id": "12345",
            "endpoint": "/api/v1/products/12345",
            "http_method": "GET",
            "database_query": "SELECT * FROM products WHERE id = '12345'",
            "query_execution_time": "15ms",
            "stack_trace": """
  File "/app/routers/products.py", line 45, in get_product
    product = db.query(Product).filter(Product.id == product_id).first()
  File "/app/routers/products.py", line 47, in get_product
    raise HTTPException(status_code=404, detail="Product not found")
            """.strip(),
            "user_id": "user_3f8a9c1d",
            "referrer": "https://example.com/shop/category/electronics",
            "search_history": [
                {"id": "12343", "found": True, "timestamp": "2024-01-15T10:42:00Z"},
                {"id": "12344", "found": True, "timestamp": "2024-01-15T10:43:00Z"},
                {"id": "12345", "found": False, "timestamp": "2024-01-15T10:44:00Z"}
            ],
            "possible_reasons": [
                "Product deleted recently",
                "Product ID typo in client",
                "Product not yet synchronized from inventory system",
                "Cache invalidation issue"
            ]
        },
        "metrics": {
            "404_errors_last_hour": 67,
            "most_requested_missing_ids": ["12345", "98765", "55555"],
            "cache_hit_rate": "78%",
            "database_query_success_rate": "94%"
        },
        "suggested_checks": [
            "Verify resource ID is correct",
            "Check if resource was recently deleted",
            "Review cache synchronization",
            "Implement soft delete with proper error messages",
            "Add suggestions for similar resources",
            "Check data replication lag between services"
        ]
    },
    {
        "name": "MemoryError",
        "status_code": 500,
        "detail": "Service out of memory. Unable to process large dataset.",
        "severity": "error",
        "context": {
            "service": "analytics-service",
            "endpoint": "/api/v1/reports/generate",
            "operation": "generate_annual_report",
            "memory_stats": {
                "total_memory": "4GB",
                "used_memory": "3.9GB",
                "available_memory": "100MB",
                "memory_threshold": "3.5GB"
            },
            "dataset_size": {
                "rows": 5000000,
                "estimated_memory": "4.2GB",
                "data_range": "2023-01-01 to 2023-12-31"
            },
            "stack_trace": """
  File "/app/services/analytics.py", line 234, in generate_report
    data = pd.read_csv(file_path)
  File "/usr/local/lib/python3.11/site-packages/pandas/io/parsers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
MemoryError: Unable to allocate array with shape (5000000, 50)
            """.strip(),
            "pod_resources": {
                "cpu_limit": "2 cores",
                "memory_limit": "4GB",
                "cpu_usage": "180%",
                "memory_usage": "97.5%"
            },
            "request_parameters": {
                "report_type": "annual_summary",
                "year": 2023,
                "include_details": True,
                "format": "PDF"
            }
        },
        "metrics": {
            "avg_report_size": "2.1GB",
            "memory_oom_kills_today": 5,
            "avg_memory_usage": "85%",
            "peak_memory_time": "09:00-10:00 UTC"
        },
        "suggested_checks": [
            "Implement data pagination/chunking",
            "Increase pod memory limits",
            "Use streaming/iterative processing",
            "Implement data sampling for large datasets",
            "Add queue system for heavy reports",
            "Optimize data structures and algorithms",
            "Consider using distributed processing (Spark, Dask)"
        ]
    },
    {
        "name": "DeadlockError",
        "status_code": 500,
        "detail": "Database deadlock detected. Transaction rolled back.",
        "severity": "warning",
        "context": {
            "service": "transaction-service",
            "database": "PostgreSQL",
            "deadlock_details": {
                "process_1": {
                    "pid": 12345,
                    "query": "UPDATE accounts SET balance = balance - 100 WHERE id = 'acc_001'",
                    "waiting_for": "acc_002",
                    "lock_type": "row exclusive"
                },
                "process_2": {
                    "pid": 12346,
                    "query": "UPDATE accounts SET balance = balance + 100 WHERE id = 'acc_002'",
                    "waiting_for": "acc_001",
                    "lock_type": "row exclusive"
                }
            },
            "stack_trace": """
  File "/app/services/transaction.py", line 156, in transfer_funds
    db.execute(update_sender_query)
  File "/app/services/transaction.py", line 158, in transfer_funds
    db.execute(update_receiver_query)
psycopg2.extensions.TransactionRollbackError: deadlock detected
DETAIL: Process 12345 waits for ShareLock on transaction 7890; blocked by process 12346.
            """.strip(),
            "transaction_id": "txn_deadlock_7d8f",
            "involved_tables": ["accounts", "transaction_log"],
            "isolation_level": "READ COMMITTED",
            "retry_attempt": 1,
            "max_retries": 3
        },
        "metrics": {
            "deadlocks_last_hour": 8,
            "avg_transaction_time": "250ms",
            "concurrent_transactions": 450,
            "deadlock_retry_success_rate": "85%"
        },
        "suggested_checks": [
            "Implement consistent lock ordering",
            "Add retry logic with exponential backoff",
            "Review transaction isolation levels",
            "Minimize transaction duration",
            "Consider optimistic locking",
            "Use SELECT FOR UPDATE NOWAIT",
            "Analyze and optimize query execution order"
        ]
    }
]

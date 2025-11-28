"""
DEPRECATED: User management routes have been consolidated.

All user endpoints are now in: app/user_manegment/roughts/roughts.py

Consolidated Routes (under /user prefix):
  - GET    /user/get                    - Get all users
  - GET    /user/get/paginated          - Get users with pagination (query: limit, page)
  - POST   /user/add                    - Add a new user
  - GET    /user/getUser                - Get current user (requires token)
  - POST   /user/checkNumber            - Check if phone exists
  - PATCH  /user/update-user            - Update current user (requires token)
  - PUT    /user/update-basic           - Update user basic info (legacy endpoint)
  - DELETE /user/delete/<user_id>       - Delete user (requires token)
  - PUT    /user/upload-avatar          - Upload avatar (requires token)
  - GET    /user/avatar/<filename>      - Get avatar file
  - GET    /user/file/<filename>        - Get file from uploads

This file is kept for reference. See CONSOLIDATION_SUMMARY.md for details.
"""

# This file is no longer used. All routes have been moved to app/user_manegment/roughts/roughts.py

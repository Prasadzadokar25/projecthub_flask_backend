"""
Compatibility shim for user model.

The canonical user management logic is now in `app.user_manegment.controller.user_controller.UserController`.
This module re-exports it as `UserModel` for backward compatibility with legacy code.
"""

from app.user_manegment.controller.user_controller import UserController

# Export UserController as UserModel for backward compatibility
UserModel = UserController

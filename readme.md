# User Management System - IS601 Final Project

## Introduction
Developed under the guidance of Professor William Keith, the User Management System showcases the capabilities of modern web technologies as a part of the IS601 course. This open-source project utilizes the 12-Factor App methodology and Agile Manifesto principles to provide a hands-on learning experience in software development, preparing students to build scalable, maintainable, and production-ready applications.

### Key Methodologies
- **12-Factor App Methodology**: Teaches important software engineering concepts such as codebase management, dependency control, and environmental consistency.
- **Agile Practices**: Encourages an environment of teamwork, iterative development, and continuous customer collaboration.
- **Industry Standards**: Focuses on coding standards like PEP 8 and introduces critical practices such as error handling and dependency injection.

## Features and Issues Addressed
- **Profile Picture Upload with Minio**: Enhances user profile management by allowing users to securely upload and store profile pictures using Minio. [More about this feature](https://github.com/NidhishVyas/user_management/pull/6)
- **Issues solved**:
  - Code Update: Automatic Verification Email on User Registration [Issue Link](https://github.com/NidhishVyas/user_management/pull/1)
  - Update to User Response Model: Status Code 400 for Duplicate Nickname Registration [Issue Link](https://github.com/NidhishVyas/user_management/pull/2)
  - Ensuring Non-Negative Skip and Positive Limit Parameters [Issue Link](https://github.com/NidhishVyas/user_management/pull/3)
  - Implementation of Password Validation [Issue Link](https://github.com/NidhishVyas/user_management/pull/4)
  - Enhanced URL Validation with Updated Regex Pattern [Issue Link](https://github.com/NidhishVyas/user_management/pull/5)

## Test Cases
Included test cases cover a variety of functionality and validation scenarios:
- `test_email_verification_test`
- `test_create_user_duplicate_nickname`
- `test_user_base_nickname_valid`
- and more...

## Deployment and Repository Links
- [GitHub Commits](https://github.com/NidhishVyas/user_management/commits/main/)
- [GitHub Deployments](https://github.com/NidhishVyas/user_management/deployments)
- [GitHub Actions](https://github.com/NidhishVyas/user_management/actions)
- [Docker Hub](https://hub.docker.com/repository/docker/nidhish1312/user_management/general)

## MiniO S3 Bucket Screenshot
Configured S3 bucket with a image file using Minio; the screenshot below illustrates this setup.
![MiniO Console Screenshot](/image.png)

## Technologies Integrated
- **FastAPI**: For high-performance API development.
- **SQLAlchemy**: For database management.
- **PostgreSQL**: For handling large-scale databases.
- **MinIO**: For managing large datasets efficiently.
- **OAuth2**: For secure user authentication.
- **Docker**: For containerization and consistent environments.
- **Alembic**: For database migrations and versioning.

## Conclusion
This project served as a bridge between theoretical knowledge and practical application, providing a deep dive into software development. I have gained valuable skills in technologies and best practices that are crucial in the software industry, equipping me for challenges in fields like software engineering, cybersecurity, and DevOps.


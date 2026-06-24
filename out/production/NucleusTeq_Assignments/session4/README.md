# TODO Application

Spring Boot 3.x TODO REST API built with Java 17, Maven, Spring Data JPA, Bean Validation, and an H2 in-memory database.

## Requirements Covered

- Strict `Controller -> Service -> Repository` layered architecture
- Constructor injection only
- DTO-based API responses and requests
- Manual DTO mapping without Lombok or MapStruct
- JPA entity with `@Entity`, `@Id`, and `@Table`
- H2 in-memory database
- Request validation with `@Valid`, `@NotNull`, and `@Size`
- Basic global exception handling
- Unit tests with JUnit 5 and Mockito

## Project Structure

```text
session4
|-- pom.xml
|-- README.md
|-- postman
|   `-- todo-application.postman_collection.json
`-- src
    |-- main
    |   |-- java/com/garv/todo
    |   |   |-- TodoApplication.java
    |   |   |-- controller/TodoController.java
    |   |   |-- dto/ErrorResponse.java
    |   |   |-- dto/TodoDTO.java
    |   |   |-- dto/TodoResponseDTO.java
    |   |   |-- entity/Todo.java
    |   |   |-- entity/TodoStatus.java
    |   |   |-- exception/GlobalExceptionHandler.java
    |   |   |-- exception/InvalidStatusTransitionException.java
    |   |   |-- exception/ResourceNotFoundException.java
    |   |   |-- mapper/TodoMapper.java
    |   |   |-- repository/TodoRepository.java
    |   |   `-- service/TodoService.java
    |   `-- resources/application.properties
    `-- test/java/com/garv/todo
        |-- TodoApplicationTests.java
        `-- service/TodoServiceTest.java
```

## API Endpoints

| Method | URL | Description |
| --- | --- | --- |
| `POST` | `/todos` | Create a TODO |
| `GET` | `/todos` | Get all TODOs |
| `GET` | `/todos/{id}` | Get TODO by ID |
| `PUT` | `/todos/{id}` | Update TODO |
| `DELETE` | `/todos/{id}` | Delete TODO |

## Request Body

```json
{
  "title": "Complete assignment",
  "description": "Build Spring Boot TODO application",
  "status": "PENDING"
}
```

`status` is optional during creation. If omitted, it defaults to `PENDING`.

## Status Rules

Allowed status changes:

- `PENDING` to `COMPLETED`
- `COMPLETED` to `PENDING`

Submitting the same status again is treated as no status change.

## Run the Application

```bash
mvn spring-boot:run
```

The application starts at:

```text
http://localhost:8080
```

H2 Console:

```text
http://localhost:8080/h2-console
```

JDBC URL:

```text
jdbc:h2:mem:todo_db
```

## Run Tests

```bash
mvn test
```

## IntelliJ IDEA Setup

Open this project as a Maven project from the `session4` folder only.

Recommended steps:

1. Close the currently opened project in IntelliJ.
2. Choose `File -> Open`.
3. Select `session4/pom.xml`, not the parent `Garv_Singh_Chouhan_java_training` folder.
4. Click `Open as Project`.
5. Wait for Maven dependencies to finish importing.
6. If packages still show red, right-click `pom.xml` and choose `Maven -> Reload Project`.

Correct source roots after import:

- `src/main/java` should be marked as `Sources Root`.
- `src/test/java` should be marked as `Test Sources Root`.
- Do not mark `src/main` as a source root.

If IntelliJ suggests package names like `java.com.garv.todo`, the project was imported incorrectly. Remove the module from IntelliJ and reopen `session4/pom.xml` as a Maven project.

The build errors from `session1`, `session2`, or `session3` are unrelated to this Spring Boot assignment. Build and run only the Maven project inside `session4`.

## File Explanation

- `pom.xml`: Maven configuration with Spring Boot 3.x, Java 17, JPA, Validation, H2, and test dependencies.
- `TodoApplication.java`: Main Spring Boot entry point.
- `TodoController.java`: REST controller that receives HTTP requests and delegates work to the service.
- `TodoService.java`: Business logic layer for create, read, update, delete, default status, and status transition handling.
- `TodoRepository.java`: Spring Data JPA repository for database access.
- `Todo.java`: JPA entity mapped to the `todos` table.
- `TodoStatus.java`: Enum containing `PENDING` and `COMPLETED`.
- `TodoDTO.java`: Request DTO with validation rules.
- `TodoResponseDTO.java`: Response DTO returned by APIs so entities are not exposed directly.
- `TodoMapper.java`: Manual mapper for DTO/entity conversion.
- `ResourceNotFoundException.java`: Custom exception for missing TODO records.
- `InvalidStatusTransitionException.java`: Custom exception for invalid status changes.
- `GlobalExceptionHandler.java`: Centralized JSON error handling for validation, not found, bad request, and general errors.
- `ErrorResponse.java`: Common JSON error response model.
- `application.properties`: H2, JPA, and application configuration.
- `TodoApplicationTests.java`: Verifies the Spring context loads.
- `TodoServiceTest.java`: Unit tests for service-layer behavior using JUnit and Mockito.
- `postman/todo-application.postman_collection.json`: Postman collection covering all required API endpoints.

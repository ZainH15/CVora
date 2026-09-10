# AI CV Analyser

#### Video Demo
[Video Demo](https://youtu.be/6kNeDFZioLs)

#### Description

AI CV Analyser is a web application designed to provide users with a quick and simple assessment of their CV. The application allows a user to upload a CV in PDF format, extracts the text from the document, calculates a basic numerical score using Python, and then sends the extracted CV content to an AI model for qualitative feedback.

The project was created as my CS50x Final Project. The main goal was to build a practical application that combines traditional programming techniques with an AI API while keeping the application simple, focused, and easy to use.

Many CV analysis tools are built around complex recruitment systems, accounts, job matching, databases, and other features. I deliberately chose not to build those features because they were not necessary for the core problem I wanted to solve. Instead, AI CV Analyser focuses on one straightforward workflow: upload a CV and receive useful feedback.

The application provides two main types of results. First, it calculates an overall score out of 100 using a Python-based scoring system. Second, it uses the OpenAI API to generate more detailed feedback about the content of the CV. The AI feedback covers the CV's main strengths, main weaknesses, specific improvements that could be made, and an overall assessment.

The application is designed to be quick to use. A user does not need to create an account, enter personal information into a database, or configure a complicated profile. They simply upload their CV and wait while it is processed.

#### How It Works

The application follows a relatively simple pipeline:

1. The user selects a CV in PDF format.
2. The browser sends the PDF to the Flask server.
3. Python saves the uploaded file temporarily in the `uploads/` directory.
4. PyPDF extracts text from the PDF.
5. Python analyses the extracted text and calculates a numerical score.
6. The extracted CV text is sent to the OpenAI API for qualitative analysis.
7. The AI generates general feedback about the CV.
8. Flask sends the score and feedback to the results page.
9. The uploaded CV is deleted from the server after processing.

The temporary-file deletion is particularly important because CVs can contain personal information. The application does not need to keep the uploaded document after the analysis has been completed. The file is therefore removed using a `finally` block so that the cleanup happens even if an error occurs while processing the CV.

#### Python Scoring System

The numerical score is calculated independently from the AI feedback. This was a deliberate design choice because it means the application has a deterministic programming component rather than relying entirely on the AI model.

The application begins with a score of zero and checks the extracted CV text for several common sections and characteristics.

The current scoring system awards points for:

- An email address being present.
- An education section being present.
- A skills section being present.
- An experience section being present.
- A projects section being present.
- Having at least 1,000 characters of extracted CV text.
- Having at least 2,000 characters of extracted CV text.
- Containing numerical information.

The score is capped at 100.

This scoring system is intentionally simple. It is not intended to determine whether a person will get a job or to provide a professional recruitment assessment. Instead, it provides the user with a basic numerical indication based on the structure and amount of information detected in their CV.

#### AI Analysis

The qualitative part of the application uses the OpenAI API.

After the PDF text has been extracted, the application sends the CV content to an OpenAI model with instructions to act as a professional CV reviewer. The model is asked to provide four types of feedback:

1. Main strengths.
2. Main weaknesses.
3. Specific improvements.
4. Overall assessment.

The AI is used for general CV feedback rather than job matching. The application does not compare the CV against a job description, calculate a recruitment probability, or make decisions about whether someone should be hired.

This separation between the Python scoring system and the AI analysis was an important design decision. Python handles the predictable numerical analysis, while the AI handles the more subjective task of interpreting the CV and producing useful written feedback.

The API key is not stored directly in the source code. It is provided through the `OPENAI_API_KEY` environment variable. This prevents the secret API key from being included in the GitHub repository.

#### Technologies Used

The project was built using the following technologies:

**Python**
Python is responsible for the application's backend logic, including file handling, PDF processing, scoring, and communication with the OpenAI API.

**Flask**
Flask is the web framework used to create the application and handle HTTP requests. It manages the upload route and renders the HTML templates containing the application's interface and results.

**HTML**
HTML provides the structure of the application's pages, including the CV upload form, loading screen, score display, and feedback section.

**CSS**
CSS is used to create the visual design of the application. The interface was designed to be clean and modern while remaining relatively simple.

**JavaScript**
A small amount of JavaScript is used on the upload page to display a loading screen and animated spinner when the user submits their CV for analysis.

**PyPDF**
PyPDF is used to read uploaded PDF documents and extract their text so that the application can analyse their contents.

**OpenAI API**
The OpenAI API is used to generate qualitative feedback about the extracted CV text.

#### Files and Design

The project is organised into a small number of files and directories:

`app.py`
Contains the Flask application, CV upload handling, PDF text extraction, Python scoring system, OpenAI API request, and temporary-file cleanup.

`templates/index.html`
Contains the main upload page where the user selects their CV.

`templates/results.html`
Displays the numerical score and AI-generated feedback after the CV has been analysed.

`static/style.css`
Contains the styling for the application's interface, including the upload card, buttons, score circle, feedback area, and loading screen.

`uploads/`
Used as temporary storage for uploaded CV files while they are being processed. Files are deleted after processing.

The project intentionally does not use a database. There is no need to permanently store users or CVs because the application does not require accounts or long-term data storage.

#### User Interface

The user interface was designed around simplicity. The homepage presents the user with a central upload area and a clear button for starting the analysis.

Once the user submits a CV, a full-screen loading interface appears with a rotating circle. This provides visual feedback because PDF extraction and AI processing can take several seconds.

After processing is complete, the user is taken to a results page. The numerical score is presented prominently inside a circular element, followed by the AI feedback in a readable text area. A button is also provided to allow the user to analyse another CV.

The interface therefore follows a simple three-stage experience: upload, processing, and results.

#### Privacy and Temporary Files

An important design decision was to avoid permanently storing uploaded CVs.

CVs commonly contain personal information such as names, addresses, phone numbers, email addresses, education history, and employment history. Since the application does not need this information after the analysis has been completed, uploaded files are deleted once processing finishes.

The application also does not provide user accounts or a database, meaning there is no stored user profile or CV history.

The OpenAI API receives the extracted text because it is required to generate the qualitative analysis. Users should therefore understand that the CV content is processed by the external AI service as part of the application's functionality.

#### Running the Application

To run the application locally, Python and the required packages must be installed.

The OpenAI API key must be supplied as an environment variable rather than being written into the Python source code.

For example:

```bash

```

The application can then be started using Flask.

Once the Flask development server is running, the user can open the local address provided by Flask in their browser and upload a PDF CV.

#### Design Choices

The main design choice throughout the project was to keep the application focused on its core purpose.

I considered features such as user accounts, databases, job-description matching, dashboards, and CV history, but these would have significantly increased the complexity of the project without being necessary for the basic problem being solved.

Instead, I focused on building a complete working application from beginning to end. The final application demonstrates file uploading, server-side processing, PDF text extraction, algorithmic scoring, API integration, AI-generated feedback, frontend design, JavaScript interaction, and temporary file management.

This approach also made it possible to clearly understand how each component contributes to the final application rather than hiding the functionality behind a large framework or complex architecture.

#### AI Assistance

AI tools were used during the development of this project as development assistance. They were used to help explain programming concepts, troubleshoot errors, suggest implementation approaches, and assist with parts of the development process.

The final application was developed and tested as my own project, and I made the decisions about the application's purpose, features, structure, scoring approach, user interface, and overall design.

The OpenAI API itself is also a functional component of the finished application. It is used specifically to analyse uploaded CV text and generate general feedback for the user.

# Final Project

This is the first project.

To begin with I'm building a login screen. I will be using the model from TutorialsPoint as a framework.


## Final Project Course Description
For the final project you will have three different options.
Hybrid Project

For the hybrid project you will need to make a REST API back-end that is on a live publicly accessible cloud provider.
Backend Portion

    The backend must have at least 1 entity with 4 or more properties
    The backend must also meet at least one of the following requirements
        User accounts are supported (ie. there is data tied to specific users that only they can see or modify) and they are tied to a 3rd party provider. You could use OAuth to access basic account info or you could use something like OpenIDConnect for authentication. You should not simply handle all account creation and management yourself.
        There is additional entity with 4 or more properties that is related to the original entity and the items can be added or removed from the relationship (like books being checked out to customers)
    It needs to model different data than the one for the homework
    It must use a non-relational database on a cloud provider (Google App Engine with NDB is recommended)
    It must meet REST requirements of using resource based URLs and representations of things via links

Mobile portion

    The front end must be a native mobile front end.
    It should interact with the backed via HTTP calls
    It should be possible to add and modify at least 4 properties on each entity
    It should be possilble to add and remove entire entities

Deliverables

    To demonstrate it works you must submit a video that shows adding, removing and updating objects
        If accounts are used it must show data added via one account, a 2nd account should log in and not be able to see the data, the original account should log it and show the data persisted
        If a relationship is implemented, things should be added and removed from the relationship and the results should be seen on the mobile device
    You should submit the source code for the mobile and backends in a single zip file, with the build folders removed to save space.
    You should include a PDF that includes all your REST URLs and which verbs can be used with them

Cloud Only Project

For this option you will only build a cloud back-end on a live publicly accessible cloud provider.

    You need to implement a REST API
    User accounts are supported (ie. there is data tied to specific users that only they can see or modify) AND the account system uses 3rd party provider, there should be able to be an arbitrary number of accounts. Accounts *must* have access to some amount of account specific information that only they can either access or modify.
    There should be at least 2 entities and they should have at least 4 properties each
    You must also implement one of the following
        There should be at least one relationship between entities
        It needs to meaningfully use a 3rd party API for something other than authentication (for example connecting to a stock market API to get stock data or a weather service to pull weather data)

Deliverables

    You should include a full set of Postman tests that show adding, deleting, updating and removing entities (every applicable verb should be used)
        This should demonstrate adding, viewing and removing things in a relationship (if applicable)
        You will need to use some more advanced features of postman to do this because you will need to pull variable names and save them to variables
    You should include a PDF
        With all the routes used for your API including which verbs work for them
        A description of the 3rd party service you used
    You should include a video of the tests being run in case we are unable to run or interpret the results.
    You should include a zip of your source code

Mobile only option

For this option you will make a mobile front end only

    It must connect to a 3rd party API via OAuth 1.0 or 2.0
    It must be a native mobile app
    It should allow the user to log out and for a different user to log into the app
    The user should be able to both view, create and edit data via the app (this will vary significantly on the API used). The data must be stored and accessed via the API.
    It should be possible to meaningfully use data from at least one of
        The phone camera
        The phone location
        A SQLite database on the phone
    It cannot use an API that was already used in the class (using Google for OAuth is OK, but you should not use something like Google+ as the primary API as it was already covered in class)

Deliverables

    You should include a video that shows
        A user logging in, viewing, adding and editing data
        Closing the app
        Opening it again to show the data has persisted with the connected API
        Logging out
        Repeating the above steps with a different user
        You must demonstrate the use of the extra features within the app (eg. while in the app, take a photo and use it as a profile picture or use the GPS data to send your location
    You should include a PDF that briefly describes the API you used and includes links to its documentation
    You should include your source files with the build folders removed


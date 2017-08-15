# My parsing of the assignment description.

Implement a local android database.

Write text and location information to said database. 

Requires permission handling, location and database access.

App Requirements:

A text input field submitted by a button.

Text field saved to a SQLite database. 

Latitude and Longitude from the phone's GPS should be saved and displayed in the same row. 

If location access given, use phone location.
Else, use location of 44.5 and -123.2, the coordinates of OSU.


All past text entries should be listed. The list can be on the same page as entry, or not.

Submit a video:

    - Show the starting state of the data. 
    - Add 3 entries without permission.
    - Add 3 with permission.
    - Close and reopen the app.
    - Show that the data persists.

Submit a zip of the source.

# Notes from the lecture.

How are permissions requested?

When do permisssions need to be checked?

How can location data be gathered?

How are SQLite databases created?

How are SQLite databases used?

How can we use cursors from SQLite database queries?


## Permissions
From here down are notes and selections from Oregon State University's CS 496 (Mobile and Cloud Development) - Summer, 2017.

The first step is to declare permissions that might be needed in the manifest file.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="net.justinwolford.quotetracker">

<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
.
.
.
```

Permissions should be checked every time before use as the user can revoke permissions.

Permissions can be checked via `ContextCompat.checkSelfPermission(context, permission_in_question)`. 

To get a `true` or `false` response:
```java
ContextCompat.checkSelfPermission(this,
    Manifest.permission.READ_CONTACTS)
== PackageManager.PERMISSION_GRANTED)
```

If permissions aren't granted, then ask for permissions using: `ActivityCompat.requestPermissions`.

An example may look like...

```java
@Override
public void onRequestPermissionsResult(int requestCode,
        String permissions[], int[] grantResults) {
    switch (requestCode) {
        case MY_PERMISSIONS_REQUEST_READ_CONTACTS: {
            // If request is cancelled, the result arrays are empty.
            if (grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                // permission was granted, yay! Do the
                // contacts-related task you need to do.

            } else {

                // permission denied, boo! Disable the
                // functionality that depends on this permission.
            }
            return;
        }

        // other 'case' lines to check for other
        // permissions this app might request
    }
}   
```



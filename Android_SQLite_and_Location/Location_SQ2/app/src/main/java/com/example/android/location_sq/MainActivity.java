package com.example.android.location_sq;

import android.app.Dialog;
import android.content.ContentValues;
import android.content.Context;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.location.Location;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.Manifest;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.helper.ItemTouchHelper;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.example.android.location_sq.database.LocationDBHelper;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.example.android.location_sq.database.LocationDBContract.*;

public class MainActivity extends AppCompatActivity implements LocationListener, GoogleApiClient.OnConnectionFailedListener, GoogleApiClient.ConnectionCallbacks {

    // Location Vars
    private GoogleApiClient mGoogleApiClient; // Used to access location services.
    private LocationRequest mLocationRequest; // Used to request location updates.
    private Location mLastLocation = new Location(""); // Stores location upon receipt.
    private static final int REQUEST_LOCATION = 15; // Used to indicate which request has come back.
    private final String mLogTag = "Joshua's Main Activity:";
    private Toast mLocationDeniedToast;

    // UI Vars
    private TextView mTV_Longitude; // Location TextView
    private TextView mTV_Latitude; // Location TextView
    private LocationListAdapter mLocationAdapter;

    // Database Vars
    private SQLiteDatabase mLocationDB;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /* * Location Stuffs * */
        // Get Lat Lon TextViews...
        mTV_Latitude = (TextView) findViewById(R.id.tv_Latitude);
        mTV_Longitude = (TextView) findViewById(R.id.tv_Longitude);

        // Build the GoogleApiClient.
        if (mGoogleApiClient == null) {
            mGoogleApiClient = new GoogleApiClient.Builder(this)
                    .addConnectionCallbacks(this)
                    .addOnConnectionFailedListener(this)
                    .addApi(LocationServices.API)
                    .build();
        }

        // Build location request object.
        mLocationRequest = LocationRequest.create();
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        mLocationRequest.setInterval(5000);

        /* * Database Stuffs * */
        LocationDBHelper locationDBHelper = new LocationDBHelper(this); // Creates database and table.
        mLocationDB = locationDBHelper.getWritableDatabase(); // Get the database in writable form.
        Cursor locationCursor = getAllLocations(); // Get all locations available.

        /* * Recycler View stuffs * */
        RecyclerView locationRecyclerView;
        locationRecyclerView = (RecyclerView) this.findViewById(R.id.locationsListView);
        mLocationAdapter = new LocationListAdapter(this, locationCursor);
        locationRecyclerView.setAdapter(mLocationAdapter);
        locationRecyclerView.setLayoutManager(new LinearLayoutManager(this));



        /* * Setup toast for location denied notification * */
        Context context = getApplicationContext();
        CharSequence text = "Location Disabled";
        int duration = Toast.LENGTH_SHORT;
        mLocationDeniedToast = Toast.makeText(context, text, duration);

        // COMPLETED (3) Create a new ItemTouchHelper with a SimpleCallback that handles both LEFT and RIGHT swipe directions
        // Create an item touch helper to handle swiping items off the list

        /* * Setup swipe left right to delete location. * */
        /* This uses an item touch helper attached to the locationRecyclerView */
        new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0, ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {

            // onMove override is required, but not needed.
            @Override
            public boolean onMove(RecyclerView recyclerView, RecyclerView.ViewHolder viewHolder, RecyclerView.ViewHolder target) {
                return false;
            }

            // Get the tag of the item being swiped which corresponds to the ID of the location
            // in the database then delete the item from the database using the ID. Then update the
            // recycler view.
            @Override
            public void onSwiped(RecyclerView.ViewHolder viewHolder, int swipeDir) {
                long id = (long) viewHolder.itemView.getTag();
                removeLocation(id);
                mLocationAdapter.swapCursor(getAllLocations());
            }
        }).attachToRecyclerView(locationRecyclerView);

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }



    public void addLocation(){
        addLocationToDB(mLastLocation);
        mLocationAdapter.swapCursor(getAllLocations());
    }


    private long addLocationToDB(Location location){
        long temp = 0;
        if (location == null) return temp;
        ContentValues values = new ContentValues();
        values.put(LocationDBEntry.COLUMN_LATITUDE, location.getLatitude());
        values.put(LocationDBEntry.COLUMN_LONGITUDE, location.getLongitude());
        Log.i(mLogTag, "Location added to database.");
        return mLocationDB.insert(LocationDBEntry.TABLE_NAME, null, values);
    }



    @Override
    protected void onStart() {
        mGoogleApiClient.connect();
        super.onStart();
    }



    @Override
    protected void onStop() {
        mGoogleApiClient.disconnect();
        super.onStop();
    }



    // Menu button location...
    @Override
    public boolean onOptionsItemSelected(MenuItem itemClicked) {
        if (itemClicked.getItemId() == R.id.action_locate) {
            if     (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
                    ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
                getLocationPermission();
            else addLocation();
        }
        return super.onOptionsItemSelected(itemClicked);
    }




    @Override
    public void onConnected(@Nullable Bundle bundle) {
        Log.i(mLogTag, "GoogleApiClient connected.");
    }



    @Override
    public void onConnectionSuspended(int i) { Log.i(mLogTag, "GoogleApiClient connection suspended.");}



    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Dialog errorDia = GoogleApiAvailability.getInstance().getErrorDialog(this, connectionResult.getErrorCode(), 0);
        errorDia.show();
    }


    @Nullable
    private void getLocationPermission() {
        Log.i(mLogTag, "In get location.");
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_COARSE_LOCATION, Manifest.permission.ACCESS_FINE_LOCATION}, REQUEST_LOCATION);
            return;
        }
        LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case REQUEST_LOCATION: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    getLocationPermission();

                    // Permission was granted, yay!
                    // Update the current location...

                } else {
                    // TODO: handle location denied callback stuff
                    mLocationDeniedToast.show();
                }
                return;
            }

            // other 'case' lines to check for other
            // permissions this app might request
        }
    }




    @Override
    public void onLocationChanged(Location location) {
        Log.i(mLogTag, "Location changed.");
        if (location != null) mLastLocation.set(location);
        else mTV_Longitude.setText("No Location Available");
    }


    private Cursor getAllLocations(){
        return mLocationDB.query(
                LocationDBEntry.TABLE_NAME,
                null,
                null,
                null,
                null,
                null,
                LocationDBEntry._ID
        );
    }



    private boolean removeLocation(long id){
        return (mLocationDB.delete(LocationDBEntry.TABLE_NAME, LocationDBEntry._ID + "=" + id, null) > 0);
    }

}




















package com.example.android.location_sq.database;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.example.android.location_sq.database.LocationDBContract.*;

/**
 * Created by jreed on 8/17/17.
 */

public class LocationDBHelper extends SQLiteOpenHelper {


    private static final String DATABASE_NAME = "location.db";
    private static final int DATABASE_VERSION = 1;


    public LocationDBHelper(Context context){
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }


    // When a database is created, this is called to set up the location table.
    @Override
    public void onCreate(SQLiteDatabase sqLiteDatabase) {
        final String BUILD_LOCATION_TABLE = "CREATE TABLE " + LocationDBEntry.TABLE_NAME + " (" +
                LocationDBEntry._ID              + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                LocationDBEntry.COLUMN_LATITUDE  + " FLOAT NOT NULL, " +
                LocationDBEntry.COLUMN_LONGITUDE + " FLOAT NOT NULL, " +
                LocationDBEntry.COLUMN_TIMESTAMP + " TIMESTAMP DEFAULT CURRENT_TIMESTAMP" + ");";

        sqLiteDatabase.execSQL(BUILD_LOCATION_TABLE);
    }

    //
    @Override
    public void onUpgrade(SQLiteDatabase sqLiteDatabase, int i, int i1) {

    }
}

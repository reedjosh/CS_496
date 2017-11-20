package com.hiketrack.android.hikingtracker;

public class Hiker{
    public String name;
    public int weight;
    public int height;
    public String id;

    public String toString(){
        return "Name: " + name + " Weight: " + String.valueOf(weight) + " Height: " + String.valueOf(height);
    }

}

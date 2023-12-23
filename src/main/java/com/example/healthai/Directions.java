package com.example.healthai;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

public class Directions extends AppCompatActivity implements OnMapReadyCallback {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_directions);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        // Set a specific location on the map
        LatLng location = new LatLng(37.7749, -122.4194);

        // Add a marker at the location
        googleMap.addMarker(new MarkerOptions().position(location).title("Marker Title"));

        // Move the camera to the marker location
        googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(location, 15)); // Adjust zoom level as needed
    }
}

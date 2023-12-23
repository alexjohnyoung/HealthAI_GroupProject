package com.example.healthai;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class EditGPDetailsActivity extends AppCompatActivity {

    private Button homepageButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_gp_details);
        readUserInfoFromDatabase();

        Button confirmButton = findViewById(R.id.button_confirm);
        confirmButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Get the selected user information from the spinner
                Spinner spinnerUser = findViewById(R.id.spinnerDoctor);
                String selectedUserInfo = (String) spinnerUser.getSelectedItem();

                // Pass the selected user information to the GPDetailsActivity
                Intent gpDetailsActivityIntent = new Intent(EditGPDetailsActivity.this, GPDetailsActivity.class);
                gpDetailsActivityIntent.putExtra("USER_INFO", selectedUserInfo);
                startActivity(gpDetailsActivityIntent);
            }
        });

        homepageButton = findViewById(R.id.button_homepage);


        homepageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent homescreenActivityIntent = new Intent(EditGPDetailsActivity.this, HomescreenActivity.class);
                startActivity(homescreenActivityIntent);
            }
        });
    }

    private void readUserInfoFromDatabase() {
        DatabaseReference databaseReference2 = FirebaseDatabase.getInstance().getReference("users");

        databaseReference2.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                List<String> userInfoList = new ArrayList<>();

                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    Doctor doctor = snapshot.getValue(Doctor.class);

                    // Assuming you want to display the user's name and address in the spinner
                    if (doctor != null) {
                        String userInfo = doctor.getName() + ", " + doctor.getSurname();
                        userInfoList.add(userInfo);
                    }
                }

                // Update the spinner with the dynamically fetched user information
                ArrayAdapter<String> userAdapter = new ArrayAdapter<>(EditGPDetailsActivity.this, android.R.layout.simple_spinner_item, userInfoList);
                userAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

                Spinner spinnerUser = findViewById(R.id.spinnerDoctor);
                spinnerUser.setAdapter(userAdapter);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                // Handle the error
            }
        });
    }
}

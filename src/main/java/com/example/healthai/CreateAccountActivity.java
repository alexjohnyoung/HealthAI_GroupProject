package com.example.healthai;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.FirebaseApp;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class CreateAccountActivity extends AppCompatActivity {

    private EditText firstNameEditText;
    private EditText surnameEditText;
    private EditText ppsNumberEditText;
    private EditText emailEditText;
    private EditText passwordEditText;

    private static final String TAG = "CreateAccountActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_account);

        // Find views by ID
        firstNameEditText = findViewById(R.id.firstname_text);
        surnameEditText = findViewById(R.id.surname_text);
        ppsNumberEditText = findViewById(R.id.pps_num_text);
        emailEditText = findViewById(R.id.email_text);
        passwordEditText = findViewById(R.id.password_text);
        Button createAccountButton = findViewById(R.id.create_account_button);

        createAccountButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createAccount();
            }
        });
    }

    private void createAccount() {
        // Retrieve user input
        String firstName = firstNameEditText.getText().toString().trim();
        String surname = surnameEditText.getText().toString().trim();
        String pps = ppsNumberEditText.getText().toString().trim();
        String email = emailEditText.getText().toString().trim();
        String password = passwordEditText.getText().toString().trim();

        // Validate input
        if (firstName.isEmpty() || surname.isEmpty() || pps.isEmpty() || email.isEmpty() || password.isEmpty()) {
            Toast.makeText(CreateAccountActivity.this, "Please fill in all fields", Toast.LENGTH_SHORT).show();
            return;
        }

        // Initialize Firebase
        FirebaseApp.initializeApp(this);

        // Get a reference to the "users" node in the database
        DatabaseReference databaseReferenceNew = FirebaseDatabase.getInstance().getReference("appusers");

        // Create a User object
        User newUser = new User(firstName, surname, pps, email, password);

        // Create user in Firebase Authentication
        FirebaseAuth.getInstance().createUserWithEmailAndPassword(email, password)
                .addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // User created successfully in Authentication
                            FirebaseUser user = task.getResult().getUser();
                            Log.d(TAG, "User creation successful. UID: " + user.getUid());

                            // Store additional user details in the Realtime Database
                            DatabaseReference userReference = databaseReferenceNew.child(user.getUid());
                            userReference.setValue(newUser)
                                    .addOnCompleteListener(new OnCompleteListener<Void>() {
                                        @Override
                                        public void onComplete(@NonNull Task<Void> databaseTask) {
                                            if (databaseTask.isSuccessful()) {
                                                // Data successfully stored in the database
                                                Log.d(TAG, "Data stored in Realtime Database successfully.");
                                                Toast.makeText(CreateAccountActivity.this, "Account created successfully", Toast.LENGTH_SHORT).show();
                                                clearFields();
                                                startActivity(new Intent(CreateAccountActivity.this, MainActivity.class));
                                            } else {
                                                // Handle the error
                                                Log.e(TAG, "Failed to store data in Realtime Database", databaseTask.getException());
                                                Toast.makeText(CreateAccountActivity.this, "Failed to create account", Toast.LENGTH_SHORT).show();
                                            }
                                        }
                                    });
                        } else {
                            // Handle the error
                            Log.e(TAG, "Failed to create user in Authentication", task.getException());
                            Toast.makeText(CreateAccountActivity.this, "Failed to create account", Toast.LENGTH_SHORT).show();
                        }
                    }
                });
    }

    private void clearFields() {
        firstNameEditText.setText("");
        surnameEditText.setText("");
        ppsNumberEditText.setText("");
        emailEditText.setText("");
        passwordEditText.setText("");
    }
}

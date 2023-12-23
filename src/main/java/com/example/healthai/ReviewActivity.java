package com.example.healthai;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class ReviewActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reviews);

        // Sample data
        List<Review> reviewList = getSampleReviewData();

        // RecyclerView setup
        RecyclerView recyclerView = findViewById(R.id.recyclerViewReviews);
        ReviewAdapter adapter = new ReviewAdapter(reviewList);
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
    }

    // Method to generate sample review data
    private List<Review> getSampleReviewData() {
        // Implement this method to provide actual review data
        // You can retrieve reviews from a database or any other source
        // For the sake of this example, I'll create some dummy data
        List<Review> reviews = new ArrayList<>();
        reviews.add(new Review("Alice Johnson", "The health AI tool is incredibly accurate and user-friendly. It gives me peace of mind to assess my health at my fingertips. 5 stars!", 4.8));
        reviews.add(new Review("Bob Anderson", "Using this app, I quickly contacted my GP and received a prompt response. It's a game-changer for managing my health. Highly recommend!", 4.9));
        reviews.add(new Review("Catherine Williams", "This app is a lifesaver! I updated my insurance details hassle-free and can now easily access my medical records. So convenient!", 5.0));
        reviews.add(new Review("David Miller", "The health assessment feature is intuitive, providing valuable insights. Plus, the option to contact my GP seamlessly is a great addition. 5 stars!", 4.7));
        reviews.add(new Review("Emma Davis", "The app's design is sleek, and the medical record viewing feature is secure and convenient. Excellent tool for managing my health information.", 4.5));
        reviews.add(new Review("Frank Wilson", "Fast and efficient service for updating insurance details. The peace of mind this app gives is invaluable. I recommend it to everyone.", 4.6));
        reviews.add(new Review("Grace Taylor", "My experience using the app has been exceptional. Updating insurance details and accessing medical records is a breeze. Well done!", 4.9));
        reviews.add(new Review("Henry Brown", "I appreciate the simplicity of the health assessment tool. It's a reliable way to gauge my health status. Good job on this app!", 4.4));
        reviews.add(new Review("Isabel Martinez", "The option to contact my GP directly through the app is a game-changer. It saves time and ensures quick healthcare access. Truly impressive.", 5.0));
        reviews.add(new Review("Jack Robinson", "This app is a must-have for anyone focused on their health. Quick GP contact and seamless insurance updates make it stand out. 5 stars!", 4.8));
        reviews.add(new Review("Kelly White", "User-friendly interface and excellent support. The health assessment tool is thorough, and I feel confident using this app for my health needs.", 4.7));
        reviews.add(new Review("Leo Garcia", "The app's sleek design complements its high-performance features. Contacting my GP and managing insurance details has never been easier. Well done!", 5.0));
        reviews.add(new Review("Mia Lee", "The app provides a good overview of my health status. It's a reliable companion, and I appreciate the effort put into creating a comprehensive tool.", 4.3));
        reviews.add(new Review("Noah Hall", "The app exceeded my expectations. Quick response from my GP and the ability to view medical records make it a valuable addition to my health routine.", 4.9));
        reviews.add(new Review("Olivia Smith", "Sturdy construction and well-designed features. The health AI tool is a reliable choice for those who prioritize their health. Highly recommended!", 4.5));
        reviews.add(new Review("Peter Johnson", "Responsive customer support addressed my queries quickly. The app's features are robust, and I feel more in control of my health management.", 4.7));
        reviews.add(new Review("Quinn Adams", "The health AI tool is exactly as described. I appreciate the attention to detail, making it a trustworthy resource for health assessments.", 4.6));
        reviews.add(new Review("Rachel Carter", "Highly recommend this app to everyone. The health AI tool is a game-changer, and the option to contact my GP instantly is a huge plus.", 5.0));
        reviews.add(new Review("Samuel Taylor", "The app lived up to the hype. The health assessment tool is impressive, and it seamlessly integrates with my medical records. A must-have!", 4.9));
        reviews.add(new Review("Tina Walker", "Good value for money. The app exceeded my expectations for managing my health. The features are robust, and I feel more confident in my health decisions.", 4.8));

        return reviews;
    }
}

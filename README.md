# Crowd-Funding Web Application Documentation 

## Introduction
  Crowdfunding is a method of raising funds for a project or venture by soliciting small contributions from a large number of people, typically through online platforms. 
  This project aims to create a web platform for initiating fundraising campaigns.

## Features
### Authentication System
   - Registration: Users can sign up by providing basic information such as first name, last name, email, password, mobile phone number, and profile picture.
   - Activation Email: Upon registration, users receive an activation email with a link to activate their account. --> Users cannot log in without activation, and the activation link expires after 24 hours.
   - Login: Users can log in using their email or username and password.
   - Forgot Password: Users can reset their password by requesting a password reset link via email.
   - User Profile: Users can view and edit their profile information, including projects, donations, and additional optional details.
   - Account Deletion: Users can delete their account with a confirmation message, optionally requiring password verification.

### Projects
  - Project Creation: Users can create fundraising campaigns by providing project details such as title, description, category, total target amount, images, tags, and campaign duration.
  - Donations: Users can donate to projects and view project details, including comments, ratings, and images.
  - Comments: Users can add comments to projects, with the option for replies.
  - Reporting: Users can report inappropriate projects and comments.
  - Rating: Users can rate projects.
  - Project Cancellation: Project creators can cancel campaigns if donations fall below 25% of the target amount.
  - Project Page: Project pages display project details, ratings, images, and similar projects based on tags.

### Home
   - Slider: The homepage features a slider showcasing the highest-rated ongoing projects to encourage donations.
   - Latest Projects: The latest five projects are listed on the homepage.
   - Featured Projects: The latest five featured projects, selected by admins, are displayed.
   - Category Listing: Users can browse projects by category.
   - Search Bar: Users can search for projects by title or tag.

### Admin View
   - Admins can manage categories and projects with all crud operations.

  

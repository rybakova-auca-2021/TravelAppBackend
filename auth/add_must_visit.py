import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')
django.setup()

# Import the MustVisitPlace model
from authApp.models import MustVisitPlace

# Data to be added
data = [
    {
        "name": "Skazka Canyon",
        "description": "Skazka Canyon is known for its colorful rock formations, which have been sculpted by wind and water over thousands of years. Visitors can explore the canyon on foot and marvel at its otherworldly landscapes.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709128844/TravelApp/skazka.jpg"
    },
    {
        "name": "Karakol Ski Base",
        "description": "Located near the town of Karakol, this ski resort offers excellent opportunities for winter sports enthusiasts. With its powdery snow and challenging slopes, it's a favorite destination for skiing, snowboarding, and snowshoeing.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709128942/TravelApp/karakol_ski.jpg"
    },
    {
        "name": "Tian Shan Mountains",
        "description": "As one of the world's largest mountain ranges, the Tian Shan Mountains offer endless opportunities for outdoor adventure. Visitors can explore remote valleys, climb towering peaks, and experience the rugged beauty of this stunning alpine landscape.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129009/TravelApp/tian_shan.jpg"
    },
    {
        "name": "Sary-Chelek Biosphere Reserve",
        "description": "Located in the Jalal-Abad Region, Sary-Chelek is a UNESCO biosphere reserve known for its pristine forests, crystal-clear lakes, and diverse wildlife. Visitors can hike through the reserve's lush landscapes, explore ancient walnut forests, and admire its stunning natural beauty.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129077/TravelApp/Sary-Chelek%20Biosphere%20Reserve.jpg"
    },
    {
        "name": "Arslanbob Walnut Forest",
        "description": "Located in the Jalal-Abad Region, Arslanbob is home to one of the world's largest walnut forests, covering an area of over 600,000 acres. Visitors can hike through the ancient forest, visit picturesque waterfalls, and immerse themselves in the local culture of the Uzbek and Kyrgyz communities.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129209/TravelApp/arslanbob.jpg"
    }
]

# Loop through the data and create MustVisitPlace objects
for item in data:
    MustVisitPlace.objects.create(
        name=item['name'],
        description=item['description'],
        main_image=item['main_image']
    )

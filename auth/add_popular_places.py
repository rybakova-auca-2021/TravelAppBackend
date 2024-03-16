import os
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

# Configure Django settings
import django
django.setup()

from authApp.models import PopularPlace

# Data to be added
data = [
    {
        "name": "Bishkek",
        "description": "Bishkek, the capital of Kyrgyzstan, is a modern city with a rich history. It features wide boulevards, Soviet-era architecture, and cultural landmarks like Ala-Too Square and the National Historical Museum. The city is known for its bustling bazaars, offering a variety of goods, and its proximity to scenic mountains provides opportunities for outdoor activities. Bishkek's culinary scene showcases traditional Kyrgyz cuisine alongside international dishes. Overall, Bishkek offers a vibrant mix of culture, history, and natural beauty.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129297/TravelApp/dtcthitbveqvjuadmobl.jpg"
    },
    {
        "name": "Issyk Kul Lake",
        "description": "Issyk Kul Lake is the largest lake in Kyrgyzstan, nestled at an altitude of 1609 meters above sea level. Surrounded by majestic mountain ranges, it offers breathtaking scenery and serves as a popular destination for tourists and locals alike. Known for its crystal-clear waters and sandy beaches, Issyk Kul Lake provides opportunities for swimming, sunbathing, and various water sports. Additionally, its shores are dotted with resorts, guesthouses, and yurt camps, offering accommodation options for visitors. With its serene ambiance and stunning natural beauty, Issyk Kul Lake is a must-visit destination in Kyrgyzstan.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129352/TravelApp/vqnwqgbb0casizd8utlf.jpg"
    },
    {
        "name": "Ala Archa National Park",
        "description": "Ala Archa National Park, located south of Bishkek, is renowned for its stunning mountain scenery, alpine meadows, and outdoor activities like hiking and rock climbing. It's a popular destination for nature lovers and adventure seekers alike.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129395/TravelApp/jbgly7ukoscev8alcmot.jpg"
    },
    {
        "name": "Burana Tower",
        "description": "Burana Tower, situated in the Chuy Valley of northern Kyrgyzstan, is a historic minaret dating back to the 11th century. It's a significant archaeological site and a remnant of the ancient city of Balasagun. The tower offers insight into Kyrgyzstan's rich cultural and historical heritage, attracting visitors with its unique architecture and historical significance.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129430/TravelApp/bz9kgh5u2kply6azzozq.jpg"
    },
    {
        "name": "Tash Rabat",
        "description": "Tash Rabat is a 15th-century stone caravanserai located in the At Bashy district of Naryn Province, Kyrgyzstan. It served as a key stop along the ancient Silk Road, providing shelter and accommodation for travelers and merchants. The well-preserved structure offers a glimpse into the region's rich history and its role in facilitating trade and cultural exchange during the medieval period. Today, it stands as a testament to the enduring legacy of the Silk Road in Central Asia.",
        "main_image": "https://res.cloudinary.com/ddkw90lqd/image/upload/v1709129470/TravelApp/sgj9gwq5cewwn6pv4zmj.jpg"
    }
]

# Loop through the data and create PopularPlace objects
for item in data:
    PopularPlace.objects.create(
        name=item['name'],
        description=item['description'],
        main_image=item['main_image']
    )

import asyncio
from prisma import Prisma
from prisma.enums import Role, PaymentStatus
from datetime import datetime, timedelta

from app.core.security import hash_password

async def seed():
    db = Prisma()
    await db.connect()

    user1 = await db.user.create({
        "username": "hadi",
        "email": "hadi@example.com",
        "role": Role.USER,
        "password": hash_password("hadi")
    })
    user2 = await db.user.create({
        "username": "qadir",
        "email": "qadir@example.com",
        "role": Role.USER,
        "password": hash_password("qadir")
    })

    company = await db.user.create({
        "username": "comp1",
        "email": "comp1@example.com",
        "role": Role.COMPANY,
        "password": hash_password("comp1"),
    })

    # Features
    feature1 = await db.feature.create({
        "name": "Feature 1",
        "description": "First feature",
        "companyId": company.id
    })

    feature2 = await db.feature.create({
        "name": "Feature 2",
        "description": "Second feature",
        "companyId": company.id
    })
    
    feature3 = await db.feature.create({
        "name": "Feature 3",
        "description": "3rd feature",
        "companyId": company.id
    })

    feature4 = await db.feature.create({
        "name": "Feature 4",
        "description": "4th feature",
        "companyId": company.id
    })

    # Create Plan
    plan1 = await db.plan.create({
        "companyId": company.id,
        "name": "Basic Plan",
        "description": "30-day plan",
        "cost": 1000,
        "discount": 10,
        "validity": 30
    })
    
    plan2 = await db.plan.create({
        "companyId": company.id,
        "name": "Premium Plan",
        "description": "30-day plan",
        "cost": 2000,
        "discount": 20,
        "validity": 30
    })

    # Attach Features to Plan
    await db.planfeatures.create_many(data=[
        {"planId": plan1.id, "featureId": feature1.id},
        {"planId": plan1.id, "featureId": feature2.id}
    ])
    await db.planfeatures.create_many(data=[
        {"planId": plan2.id, "featureId": feature1.id},
        {"planId": plan2.id, "featureId": feature2.id},
        {"planId": plan2.id, "featureId": feature3.id},
        {"planId": plan2.id, "featureId": feature4.id}
    ])
    
    # New Company: comp2
    comp2 = await db.user.create({
        "username": "comp2",
        "email": "comp2@example.com",
        "role": Role.COMPANY,
        "password": hash_password("comp2"),
    })

    # Create 10 Features for comp2
    comp2_features = []
    for i in range(1, 11):
        feature = await db.feature.create({
            "name": f"Feature {i}",
            "description": f"Description for feature {i}",
            "companyId": comp2.id
        })
        comp2_features.append(feature)

    # Create Bronze Plan (3 features)
    bronze = await db.plan.create({
        "companyId": comp2.id,
        "name": "Bronze Plan",
        "description": "Entry-level plan",
        "cost": 500,
        "discount": 5,
        "validity": 30
    })
    await db.planfeatures.create_many(data=[
        {"planId": bronze.id, "featureId": f.id} for f in comp2_features[:3]
    ])

    # Create Silver Plan (6 features)
    silver = await db.plan.create({
        "companyId": comp2.id,
        "name": "Silver Plan",
        "description": "Mid-level plan",
        "cost": 1000,
        "discount": 10,
        "validity": 30
    })
    await db.planfeatures.create_many(data=[
        {"planId": silver.id, "featureId": f.id} for f in comp2_features[:6]
    ])

    # Create Gold Plan (all 10 features)
    gold = await db.plan.create({
        "companyId": comp2.id,
        "name": "Gold Plan",
        "description": "All-inclusive premium plan",
        "cost": 2000,
        "discount": 20,
        "validity": 30
    })
    await db.planfeatures.create_many(data=[
        {"planId": gold.id, "featureId": f.id} for f in comp2_features
    ])

    await db.disconnect()
    print("✅ Seed complete.")
    
    


if __name__ == '__main__':
    asyncio.run(seed())

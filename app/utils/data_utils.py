import json

import bcrypt
from fastapi import UploadFile

from app.database.connect import Mongo
from app.database.schema import UserSchema
from app.middleware.token_validator import token_decode
from app.model import UserToken, ProductRegister
from app.repository.Product import Product
from app.repository.User import User
from app.router.auth import create_access_token


class InitDB:
    def __init__(self):
        self.db = Mongo.get_db()
        self.product_coll = "products"
        self.user_coll = "users"
        self.pending = "pending"

    def get_users(self):
        user1 = dict(
            email="subin@gmail.com",
            name="문수빈",
            nickname="waterbin",
            address="0x839a5b058477d8ab01233fb295dab5e4770c1f68",
            pw="test"
        )

        user2 = dict(
            email="seungik@gmail.com",
            name="이승익",
            nickname="winik",
            address="0x5df4fe4035bE351269b566D323dD06e081e871E0",
            pw="test"
        )

        user3 = dict(
            email="dowon@gmail.com",
            name="오도원",
            nickname="doonetwothree",
            address="0xdA274B79C4cc4A40337BFF8A62e69E25aeacA837",
            pw="test"
        )

        return user1, user2, user3

    async def init_user(self):
        users = self.get_users()

        for user in users:
            hash_pw = bcrypt.hashpw(user["pw"].encode("utf-8"), bcrypt.gensalt())
            user["pw"] = hash_pw
            new_user = await User.create(UserSchema(**user))

        print("유저 초기화 성공!")

    def get_token(self, i):
        user = self.get_users()[i]
        login_info = dict(email=user["email"], pw="test")

        access_token = create_access_token(
            data=UserToken(**user).dict(exclude={"pw", "created_at"})
        )
        token = dict(Authorization=f"JWT {access_token}")

        return token

    def get_product_payload(self, product_info, file, user_index):
        data = dict(product_info=json.dumps(product_info))
        product = dict(files=file, data=data, headers=self.get_token(user_index))

        return product


    async def get_user(self, i):
        token = self.get_token(i)["Authorization"]
        token_info = await token_decode(access_token=token)
        return UserToken(**token_info)

    async def init_product(self):
        await Product.create(
            file=UploadFile(filename="가습기.png", file=open("img/가습기.png", "rb")),
            product_info=ProductRegister(
                product_name="가습기",
                description="가습기입니다. 거의 새것이에요. 진짜 안 팔려고했는데 이사가게 되어서 팝니다.",
                price=0.003,
                seller_safe=True
            ),
            user=await self.get_user(0)
        )

        await Product.create(
            file=UploadFile(filename="골프채.png", file=open("img/골프채.png", "rb")),
            product_info=ProductRegister(
                product_name="골프채",
                description="골프채입니다. 진짜 추천합니다. 너무 좋아요. 이거 사용해보시면 비거리 최소 2배이상 증가합니다.",
                price=0.002,
                seller_safe=True
            ),
            user=await self.get_user(0)
        )

        await Product.create(
            file=UploadFile(filename="말하기교구.png", file=open("img/말하기교구.png", "rb")),
            product_info=ProductRegister(
                product_name="말하기교구",
                description="말하기교구입니다. 애들을 위해서 좋은 선택하셔야합니다. 애들은 항상 좋은 것, 맛있는 것들을 사용해야합니다. 애들을 위해서 구매하세요. 거의 새것입니다. 애가 커서 판매올립니다.",
                price=0.0003,
                seller_safe=False
            ),
            user=await self.get_user(0)
        )

        await Product.create(
            file=UploadFile(filename="모니터.png", file=open("img/모니터.png", "rb")),
            product_info=ProductRegister(
                product_name="컴퓨터모니터",
                description="최고주사율의 모니터입니다. 이거 사용하시면 롤티어 최소 4단계는 올라갑니다. 본인이 브론즈면 그냥 구매하세요.",
                price=0.0004,
                seller_safe=False
            ),
            user=await self.get_user(0)
        )

        await Product.create(
            file=UploadFile(filename="쇼파.png", file=open("img/쇼파.png", "rb")),
            product_info=ProductRegister(
                product_name="온가족 쇼파",
                description="온가족이 사용할 수 있는 쇼파입니다. 완전 편하고 진짜 너무 좋습니다. 일요일에 여기 누워서 티비보면 바로 낮잠 편하게 주무실 수 있습니다. 완전  강추합니다. 이사를 가게되어서 어쩔 수 없이 내놓습니다. 꼭 구매하세요.",
                price=0.001,
                seller_safe=True
            ),
            user=await self.get_user(0)
        )

        await Product.create(
            file=UploadFile(filename="스팸.png", file=open("img/스팸.png", "rb")),
            product_info=ProductRegister(
                product_name="스팸",
                description="완전 맛있는 스팸입니다. 밥이랑 김치, 스팸만 있어도 진수성찬이 안 부럽습니다. 지금 바로 구매하시고 맛있는 식사하세요! (거의 새것)",
                price=0.0002,
                seller_safe=False
            ),
            user=await self.get_user(0)
        )

        await Product.create(
            file=UploadFile(filename="자전거.png", file=open("img/자전거.png", "rb")),
            product_info=ProductRegister(
                product_name="자전거",
                description="기어 36단까지 보장하는 자전거입니다. 이거 타면 적토마가 안 부럽습니다. 완전 신나게 온천천을 달려보세요. 운동은 역시 신나는게 최고죠. 산책하는 기분으로 자전거 타면서 살도 빼고 건강도 챙기고, 스트레스도 풀고! 일석삼조 너무 좋습니다! 거의 뭐 이건 새 거라고 봐도 무방합니다.",
                price=0.001,
                seller_safe=True
            ),
            user=await self.get_user(1)
        )

        await Product.create(
            file=UploadFile(filename="전자레인지.png", file=open("img/전자레인지.png", "rb")),
            product_info=ProductRegister(
                product_name="전자레인지",
                description="자취방에서 쓰기 딱 좋은 전자레인지입니다. 이 전자레인지로 말씀드릴거 같으면 어떤 음식이든 들어왔다 나가면 완전 맛있어집니다. 오죽하면 제가 어제 먹다남은 치킨을 넣고 돌렸는데 너무 맛있어서 바로 그 자리에서 뚝딱했다 이말입니다. 무조건 사세요. 절대 후회 안 합니다.",
                price=0.001,
                seller_safe=True
            ),
            user=await self.get_user(1)
        )

        await Product.create(
            file=UploadFile(filename="책.png", file=open("img/책.png", "rb")),
            product_info=ProductRegister(
                product_name="[난 책읽기가 좋아]책",
                description="난 책읽기가 좋아 시리즈 책입니다. 너무 재밌습니다. 이거 읽으면 시간 가는 줄도 모르고 진짜 재밌게 읽을 수 있습니다. 공부도 하고 재밌고, 안 사는게 손해입니다. 거의 새 것.",
                price=0.0015,
                seller_safe=True
            ),
            user=await self.get_user(2)
        )

        await Product.create(
            file=UploadFile(filename="책장.png", file=open("img/책장.png", "rb")),
            product_info=ProductRegister(
                product_name="책장",
                description="자취방에서 쓰던 책장입니다. 이사가게 되어서 어쩔 수 없이 판매합니다. 완전 튼튼하고 좋습니다. 무조건 쓰세요. 후회 없는 선택입니다. 책 뿐만 아니라 뭐든 올려놓고, 정리할 수 있습니다. 깨끗한 집을 위해서 좋은 선택하세요.",
                price=0.001,
                seller_safe=True
            ),
            user=await self.get_user(2)
        )


    async def drop_db(self):
        coll_names = await self.db.list_collection_names()
        for coll_name in coll_names:
            await self.db.drop_collection(coll_name)

    async def init_db(self):
        await self.drop_db()
        await self.init_user()
        await self.init_product()

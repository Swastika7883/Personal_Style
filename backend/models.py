from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base

class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(Integer, primary_key=True, index=True)
    api_item_id = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)
    base_color = Column(String(50), nullable=False)
    undertone_match = Column(String(50), index=True) # Matches the column you created!
    image_url = Column(String(500), nullable=False)
    details_url = Column(String(500))
    price = Column(DECIMAL(10, 2))
    # data_source is another column you can add here if you need it.
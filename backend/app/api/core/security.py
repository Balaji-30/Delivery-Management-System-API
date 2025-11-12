from fastapi.security import OAuth2PasswordBearer

oauth2_scheme_seller =OAuth2PasswordBearer(tokenUrl="/seller/login",scheme_name="Seller Authentication")
oauth2_scheme_partner =OAuth2PasswordBearer(tokenUrl="/partner/login",scheme_name="Delivery Partner Authentication")
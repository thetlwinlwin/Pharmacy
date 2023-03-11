# Simple Pharmacy API with FASTApi

Role of a user can't be changed once it is created. Admin can create another admin but cannot destroy or update.

## [HAS TO ADD LOGGING IN PRODCUTION](https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/) AS THE SERVER WILL LIKELY TO RUN WITH GUNICORN INSTEAD OF UVICORN. **UVICORNWORKER** HAS TO EXTENDS TO ADD LOGGER

### Auth
- Front-end has to destroy refresh token once the user logout.
- refresh tokens have been saved in db in associated with user_id.
- access token time limit is **30mins** and refresh token is **30 days**.
- new refresh token is issued everytime "me/refresh" endpoint has been hit and save the new one in db.
- In case an attacker gains access to the refresh token and attempt to use it, the backend automatically detects this ***by comparing the saved one and request one*** and immediately blocks the user's account.
- If the attacker uses the refresh token before user does, in less than **30mins** after hijacking the refresh token, the user attempts a refresh, and this also results in the user's account being blocked.
- If user use refresh token after it is expired, he can simply log in again.

### Tips
- gunicorn doesn't work on window.
- For a REST-only App/API you are free to send the JWT as the response body or a cookie.
- added 

        @classmethod
        def get_name(cls):
        
    model to raise the error inside the generic type CRUDBase.

- instead of using "count" method in orm query, use func.count and scalar. count method created the sub query which can hurt the performance.

        slow = db.query(self.model).filter(self.model.
            role==UserRole.admin).count()
            
        faster = db.query(func.count(self.model.role))
            .filter(self.model.role == UserRole.admin)
            .scalar()
- Security scopes is less useful in this situation. The codes are commented out in **oauth2/oauth2.py**.
- ***ROLE BASED ACCESS CONTROL*** was implemented as UserRoleChecker in **oauth2/oauth2.py** with the help of [documentation](https://fastapi.tiangolo.com/advanced/advanced-dependencies/).
- number of admin allow to be created is limited. check in **users_routes.py -> admin_Fcreate_user**.
- instead of logging in with username, phone number has been used as it is unique and created with indexing in db.
- catching multiple exceptions.

        except (JWTError, ValidationError) as e:


### **Sqlalchemy Tips**

backref is a shortcut for configuring both parent.children and child.parent relationships at one place only on the parent or the child class (not both). ***prefer to use back_populates on both side.***

False to uselist in relationship to mimic one-to-one relationship.

ForeignKey needs to go on the child class, no matter where the relationship is placed.

If child is needed to be deleted when parent instance is deleted, declare passive_deletes in the relationship function along with on_delete param in ForeignKey.

***NOTICE THAT if passvie_deletes is True, session doesn't not emit delete statements. If passive_deletes is set to False, but ForeignKey still have the on_delete="CASCADE" params, session explicitly emits sql DELETE statement.***(This behaviour can be seen by echo=True param in create_engine function.)


There is whole session about delete in [stackoverflow](https://stackoverflow.com/a/38770040/18446081).

Self referential technique is used to nested the sub categories in ProductCategory model. "The implementation can be seen in test folder" (
- add cascade in relationship to delete all the children after the parent has been deleted.
- also add the cascade in foreign key in parent_id.
- **You cannot limit the depth**
)

There is something interesting about sqlalchemy relationship...
Imagine you have product and proudct_type. And you want to check all the available products from the product type. So, you added relationship in both class with back_populate. The logical solution to delete is that when you delete the type, the product stays. But you forget it and added nullable=False in foregin key column in product class. Then, if you delete the type, sqlalchemy will give you error. BUT.... when you don't need to check the products from product type, you didn't add the relationships in type class and no back_populate in product class. Then, in this scenario, even if foregin key column is set to not null, it will going to be null. 

### **Exception Tips**

- all exceptions are inherited from python Exception class.
- Instead of register every exception classes, abstract base class is used and every concrete exceptions are inherited from that abstract base class. generic handler was also created.  **exceptions/generic_exceptions.py**

        app = FastAPI(
        title="My Pharmacy",
            exception_handlers={
                exc.AppExceptionBase: exc.handler,
            },
        )
- for the request validation, modifying the existing handler is more efficient.
- also added dunder slots attributes to class to save some memory.
- dunder slots attribute is not needed to define in every child. watch [this](https://youtu.be/Iwf17zsDAnY).
- export the needed classes in dunder init file.


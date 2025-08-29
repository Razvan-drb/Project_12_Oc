# Epic Events Database Schema

## Database Structure

### users Table
- **id** (Integer, Primary Key)
- **full_name** (String(100), Not Null)
- **email** (String(100), Unique, Not Null)
- **password** (String(100), Not Null) - *Bcrypt hashed*
- **department** (String(20), Not Null) - *Values: management, sales, support*
- **created_at** (DateTime, Default: current timestamp)
- **updated_at** (DateTime, Default: current timestamp, On Update: current timestamp)

### clients Table
- **id** (Integer, Primary Key)
- **full_name** (String(100), Not Null)
- **email** (String(100), Not Null)
- **phone** (String(20), Not Null)
- **company_name** (String(100), Not Null)
- **commercial_contact_id** (Integer, Foreign Key → users.id)
- **created_at** (DateTime, Default: current timestamp)
- **updated_at** (DateTime, Default: current timestamp, On Update: current timestamp)

### contracts Table
- **id** (Integer, Primary Key)
- **total_amount** (Float, Not Null)
- **amount_due** (Float, Not Null)
- **is_signed** (Boolean, Default: False)
- **client_id** (Integer, Foreign Key → clients.id)
- **commercial_contact_id** (Integer, Foreign Key → users.id)
- **created_at** (DateTime, Default: current timestamp)

### events Table
- **id** (Integer, Primary Key)
- **name** (String(100), Not Null)
- **start_date** (DateTime, Not Null)
- **end_date** (DateTime, Not Null)
- **location** (String(200), Not Null)
- **attendees** (Integer, Not Null)
- **notes** (String(500))
- **client_id** (Integer, Foreign Key → clients.id)
- **contract_id** (Integer, Foreign Key → contracts.id)
- **support_contact_id** (Integer, Foreign Key → users.id)
- **created_at** (DateTime, Default: current timestamp)
- **updated_at** (DateTime, Default: current timestamp, On Update: current timestamp)

## Relationships & Business Logic

### User Roles & Permissions
- **Management**: Full access to all data, user management
- **Sales**: Client management, their own contracts/events
- **Support**: Event management for assigned events only

### Data Access Rules
1. **Read Access**: All authenticated users can read all data
2. **Write Access**: Role-based following principle of least privilege
3. **Data Ownership**: Users only modify data they own/are assigned to

### Security Measures
- ✅ Password hashing with bcrypt
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ Input validation in controllers
- ✅ Role-based access control
- ✅ Session management with expiration
# **Django Multi-Utility Suite**

## **Description**

A Django-based suite that integrates:

- **CSV Import and Export**: Upload and export data in CSV format, saving it to the database.
- **Bulk Email Sending**: Send bulk emails with attachments and customizable content.
- **Email Tracking**: Track email opens and clicks using unique IDs for each recipient.

## **Features**

1. **CSV Handling**

   - Import CSV files and save data directly to the database.
   - Export data from the database to a CSV file.
2. **Bulk Email Sending**

   - Send personalized emails to multiple recipients.
   - Attach files and embed HTML content in emails.
3. **Email Tracking**

   - Monitor email opens and link clicks in real-time.
   - View detailed tracking logs with timestamps.

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/ayazkhan1410/DjangoMultiToolbox.git

   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## **Usage**

- Access the web interface to upload/export CSV files.
- Use the bulk email feature to send emails directly from the platform.
- Track email activity with the built-in tracking system.

## **Folder Structure**

- `csv_import_export/` – Handles CSV file operations.
- `bulk_email/` – Manages bulk email sending functionality.
- `email_tracking/` – Includes tracking logic for emails.

## **License**

This project is licensed under the MIT License.

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

# Initialize CSV file for storing client data
CSV_FILE = "client_data.csv"

# Ensure the CSV file has a header if it doesn't exist
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Landlord Name", "Tenant Name", "Rental Address"])
    df.to_csv(CSV_FILE, index=False)

# Save client data to the CSV file
def save_client_data(client_data):
    """Save client data to the CSV file."""
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame(columns=["Landlord Name", "Tenant Name", "Rental Address"])

    # Convert client_data dictionary to a DataFrame
    new_row = pd.DataFrame([client_data])
    # Concatenate the new row to the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)
    # Save back to the CSV file
    df.to_csv(CSV_FILE, index=False)
    messagebox.showinfo("Success", "Client data saved successfully!")

def populate_pdf(client_data, input_pdf="Residential_Rental.pdf", output_pdf="filled_residential_rental.pdf"):
    """Populate the rental agreement PDF with client data."""
    # Create a temporary PDF to overlay the data
    temp_pdf = "temp_overlay.pdf"
    c = canvas.Canvas(temp_pdf, pagesize=letter)

    # Add text fields to the PDF
    c.drawString(100, 700, f"Landlord Name: {client_data.get('Landlord Name', '')}")
    c.drawString(100, 680, f"Tenant Name: {client_data.get('Tenant Name', '')}")
    c.drawString(100, 660, f"Rental Address: {client_data.get('Rental Address', '')}")
    c.save()

    # Merge the overlay with the original PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    overlay_reader = PdfReader(temp_pdf)

    for page_number, page in enumerate(reader.pages):
        if page_number == 0:  # Add overlay only to the first page
            overlay_page = overlay_reader.pages[0]
            page.merge_page(overlay_page)
        writer.add_page(page)

    # Save the filled PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"PDF generated and saved as {output_pdf}")
    messagebox.showinfo("Success", f"PDF saved as {output_pdf}")

# Main application class
class RealtorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Realtor Lead Management")
        self.client_data = {}
        
        # Collect Lead Information
        tk.Label(self.root, text="Residential Rental Agreement Form", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Landlord's Name:").pack()
        self.landlord_name_entry = tk.Entry(self.root)
        self.landlord_name_entry.pack()

        tk.Label(self.root, text="Tenant's Name:").pack()
        self.tenant_name_entry = tk.Entry(self.root)
        self.tenant_name_entry.pack()

        tk.Label(self.root, text="Rental Address:").pack()
        self.rental_address_entry = tk.Entry(self.root)
        self.rental_address_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_data)
        self.submit_button.pack(pady=10)

    def submit_data(self):
        """Save the input data and populate the PDF."""
        self.client_data["Landlord Name"] = self.landlord_name_entry.get()
        self.client_data["Tenant Name"] = self.tenant_name_entry.get()
        self.client_data["Rental Address"] = self.rental_address_entry.get()

        # Validate input
        if not all(self.client_data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Save to CSV
        save_client_data(self.client_data)

        # Populate the PDF
        populate_pdf(self.client_data)

        # Show success message and reset form
        messagebox.showinfo("Success", "Form submitted successfully!")
        self.reset_form()

    def reset_form(self):
        """Clear all input fields."""
        self.landlord_name_entry.delete(0, tk.END)
        self.tenant_name_entry.delete(0, tk.END)
        self.rental_address_entry.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RealtorApp(root)
    root.mainloop()

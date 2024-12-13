import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime
import os
from tkinter import *

class BusTicketSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Ticket System with Receipt")
        self.root.geometry("1000x800")
        
        # Initialize tickets list to store all tickets
        self.tickets = []
        self.ticket_counter = 1  # For generating unique ticket IDs
        
        # Dictionary to store destinations and their prices
        self.destinations = {
            "Candelaria": 100,
            "San Juan": 85,
            "Rosario": 70,
            "Ibaan": 55,
            "Balagtas": 40
        }
        
        # Variables for user input
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.payment_var = tk.StringVar()
        self.selected_destination = None
        self.selected_price = None
        
        self.setup_gui()

    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Bus Ticket System with Receipt",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # User Information Section
        info_frame = ttk.LabelFrame(main_frame, text="User Information", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.age_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Destinations Section
        dest_frame = ttk.LabelFrame(main_frame, text="Select Destination", padding="10")
        dest_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        for index, (destination, price) in enumerate(self.destinations.items()):
            btn = ttk.Button(
                dest_frame,
                text=f"{destination} - ₱{price}",
                command=lambda d=destination, p=price: self.select_destination(d, p)
            )
            btn.grid(row=index, column=0, pady=5, padx=10, sticky=tk.W)
        
        # Payment Section
        payment_frame = ttk.LabelFrame(main_frame, text="Payment", padding="10")
        payment_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(payment_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(payment_frame, textvariable=self.payment_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(payment_frame, text="Pay", command=self.process_payment).grid(row=0, column=2, padx=5, pady=5)
        
        # Display Section
        self.display_frame = ttk.LabelFrame(main_frame, text="Ticket Information", padding="10")
        self.display_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.info_label = ttk.Label(
            self.display_frame,
            text="Please select a destination and enter your information",
            font=("Helvetica", 10)
        )
        self.info_label.grid(row=0, column=0, pady=5)
        
        # Add Manage Tickets Button
        manage_btn = ttk.Button(main_frame, text="Manage Tickets", command=self.show_ticket_manager)
        manage_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def select_destination(self, destination, price):
        """Handle destination selection"""
        self.selected_destination = destination
        self.selected_price = price
        self.info_label.config(
            text=f"Selected: {destination}\nTicket Price: ₱{price}"
        )
        
    def validate_inputs(self):
        """Validate user inputs before processing payment"""
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Please enter your name")
            return False
        if not self.age_var.get().strip():
            messagebox.showerror("Error", "Please enter your age")
            return False
        try:
            age = int(self.age_var.get())
            if age <= 0 or age > 120:
                messagebox.showerror("Error", "Please enter a valid age")
                return False
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
            return False
        if not self.selected_destination:
            messagebox.showerror("Error", "Please select a destination")
            return False
        try:
            payment = float(self.payment_var.get())
            if payment <= 0:
                messagebox.showerror("Error", "Please enter a valid payment amount")
                return False
        except ValueError:
            messagebox.showerror("Error", "Payment must be a number")
            return False
        return True
        
    def process_payment(self):
        """Process payment and generate receipt"""
        if not self.validate_inputs():
            return
            
        payment = float(self.payment_var.get())
        if payment < self.selected_price:
            messagebox.showerror("Error", "Insufficient payment")
            return
            
        change = payment - self.selected_price
        receipt_text = self.generate_receipt(change)
        
        # Create ticket dictionary and add to tickets list
        ticket = {
            'id': self.ticket_counter,
            'name': self.name_var.get(),
            'age': int(self.age_var.get()),
            'destination': self.selected_destination,
            'price': self.selected_price,
            'payment': payment,
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tickets.append(ticket)
        self.ticket_counter += 1
        
        # Show receipt in a new window
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Bus Ticket Receipt")
        receipt_window.geometry("400x500")
        
        receipt_display = tk.Text(receipt_window, font=("Courier", 12), wrap=tk.WORD)
        receipt_display.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        receipt_display.insert(tk.END, receipt_text)
        receipt_display.config(state=tk.DISABLED)
        
    def generate_receipt(self, change):
        """Generate receipt text"""
        receipt = f"""
{"="*40}
         BUS TICKET RECEIPT
{"="*40}

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Passenger Information:
Name: {self.name_var.get()}
Age: {self.age_var.get()}

Ticket Details:
Destination: {self.selected_destination}
Price: ₱{self.selected_price}

Payment Information:
Amount Paid: ₱{float(self.payment_var.get()):.2f}
Change: ₱{change:.2f}

{"="*40}
Thank you for choosing our service!
{"="*40}
"""
        return receipt

    def show_ticket_manager(self):
        """Show ticket management window"""
        manager_window = tk.Toplevel(self.root)
        manager_window.title("Ticket Manager")
        manager_window.geometry("800x600")

        # Create Treeview
        columns = ('ID', 'Name', 'Age', 'Destination', 'Price', 'Payment', 'Date/Time')
        tree = ttk.Treeview(manager_window, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(manager_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load tickets
        self.load_tickets(tree)

        # Buttons frame
        btn_frame = ttk.Frame(manager_window)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Update Selected", command=lambda: self.update_ticket(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=lambda: self.delete_ticket(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=lambda: self.load_tickets(tree)).pack(side=tk.LEFT, padx=5)

    def load_tickets(self, tree):
        """Load tickets from list into treeview"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)

        # Insert tickets
        for ticket in reversed(self.tickets):  # Show newest tickets first
            values = (
                ticket['id'],
                ticket['name'],
                ticket['age'],
                ticket['destination'],
                ticket['price'],
                ticket['payment'],
                ticket['date_time']
            )
            tree.insert('', tk.END, values=values)

    def update_ticket(self, tree):
        """Update selected ticket"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a ticket to update")
            return

        ticket_id = tree.item(selected[0])['values'][0]
        
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Ticket")
        update_window.geometry("400x300")

        # Get current values
        current_values = tree.item(selected[0])['values']

        # Create entry fields
        ttk.Label(update_window, text="Name:").pack(pady=5)
        name_var = tk.StringVar(value=current_values[1])
        ttk.Entry(update_window, textvariable=name_var).pack()

        ttk.Label(update_window, text="Age:").pack(pady=5)
        age_var = tk.StringVar(value=current_values[2])
        ttk.Entry(update_window, textvariable=age_var).pack()

        ttk.Label(update_window, text="Destination:").pack(pady=5)
        dest_var = tk.StringVar(value=current_values[3])
        ttk.Entry(update_window, textvariable=dest_var).pack()

        def save_updates():
            try:
                # Find and update the ticket in the list
                for ticket in self.tickets:
                    if ticket['id'] == ticket_id:
                        ticket['name'] = name_var.get()
                        ticket['age'] = int(age_var.get())
                        ticket['destination'] = dest_var.get()
                        break
                self.load_tickets(tree)
                update_window.destroy()
                messagebox.showinfo("Success", "Ticket updated successfully!")
            except ValueError as e:
                messagebox.showerror("Error", f"Failed to update ticket: {str(e)}")

        ttk.Button(update_window, text="Save Changes", command=save_updates).pack(pady=20)

    def delete_ticket(self, tree):
        """Delete selected ticket"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a ticket to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this ticket?"):
            ticket_id = tree.item(selected[0])['values'][0]
            # Remove ticket from list
            self.tickets = [t for t in self.tickets if t['id'] != ticket_id]
            self.load_tickets(tree)
            messagebox.showinfo("Success", "Ticket deleted successfully!")

def main():
    root = tk.Tk()
    app = BusTicketSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()

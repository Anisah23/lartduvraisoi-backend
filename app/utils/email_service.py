import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Content

class EmailService:
    @staticmethod
    def send_order_confirmation(to_email, order):
        """Send order confirmation email"""
        subject = f"Order Confirmation - #{order.id}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9fafb; padding: 20px; }}
                .order-item {{ border-bottom: 1px solid #e5e7eb; padding: 10px 0; }}
                .total {{ font-weight: bold; font-size: 18px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ArtMarket</h1>
                    <h2>Order Confirmation</h2>
                </div>
                <div class="content">
                    <p>Thank you for your order! Here are your order details:</p>
                    
                    <h3>Order #{order.id}</h3>
                    <p><strong>Status:</strong> {order.status}</p>
                    <p><strong>Order Date:</strong> {order.created_at.strftime('%B %d, %Y')}</p>
                    
                    <h4>Items Ordered:</h4>
                    {"".join([f'''
                    <div class="order-item">
                        <strong>{item.artwork.title}</strong><br>
                        by {item.artwork.artist.username}<br>
                        Quantity: {item.quantity} × ${item.artwork.price}<br>
                        Total: ${item.price}
                    </div>
                    ''' for item in order.items])}
                    
                    <div class="total">
                        Total Amount: ${order.total_amount}
                    </div>
                    
                    <p>We'll notify you when your order ships.</p>
                    <p>Thank you for shopping with ArtMarket!</p>
                </div>
            </div>
        </body>
        </html>
        """

        return EmailService._send_email(to_email, subject, html_content)

    @staticmethod
    def send_order_shipped(to_email, order, tracking_number=None):
        """Send order shipped notification"""
        subject = f"Your Order Has Shipped - #{order.id}"
        
        tracking_info = ""
        if tracking_number:
            tracking_info = f"<p><strong>Tracking Number:</strong> {tracking_number}</p>"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #10B981; color: white; padding: 20px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ArtMarket</h1>
                    <h2>Order Shipped!</h2>
                </div>
                <div class="content">
                    <p>Great news! Your order has been shipped.</p>
                    <p><strong>Order #:</strong> {order.id}</p>
                    {tracking_info}
                    <p>Your artwork is on its way to you. Please allow 5-7 business days for delivery.</p>
                    <p>Thank you for your patience!</p>
                </div>
            </div>
        </body>
        </html>
        """

        return EmailService._send_email(to_email, subject, html_content)

    @staticmethod
    def _send_email(to_email, subject, html_content):
        """Send email using SendGrid"""
        if not os.getenv('SENDGRID_API_KEY'):
            print('SendGrid API key not configured')
            return False

        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            
            message = Mail(
                from_email=os.getenv('SENDGRID_FROM_EMAIL', 'noreply@artmarket.com'),
                to_emails=to_email,
                subject=subject,
                html_content=Content("text/html", html_content)
            )

            response = sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f'Email sending failed: {str(e)}')
            return False
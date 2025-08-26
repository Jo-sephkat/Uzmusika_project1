from django.shortcuts import get_object_or_404

def cart_quantity(request):
    # Assuming you have a Cart model or session-based cart
    cart = request.session.get('cart', {})
    total_quantity = sum(cart.values())  # Sum up all quantities in the cart
    return {'cart_quantity': total_quantity}


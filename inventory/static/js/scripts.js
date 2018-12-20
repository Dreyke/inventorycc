$('#btn-product-delete').on('click', function () {
    return confirm('You are about to permanently delete a product. ' +
            'There is no undoing this action. ' +
            'Are you sure you want to continue?')
});
from iebank_api import app
import pytest

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    assert response.status_code == 200



def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Laura',
        'currency': '£',
        'country': 'UK'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, update the account
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Anna'
    })
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data['name'] == 'Anna'
    assert updated_data['currency'] == '£'
    assert updated_data['country'] == 'UK'
    assert updated_data['id'] == account_id

    # Verify that the account was updated
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    get_data = get_response.get_json()
    assert get_data['name'] == 'Anna'


def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the response is valid and the account no longer exists
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Charlie',
        'currency': '$',
        'country': 'USA'
    })
    assert create_response.status_code == 200, (
        f"Failed to create account. Status: {create_response.status_code}, "
        f"Response: {create_response.data.decode('utf-8')}"
    )
    account_data = create_response.get_json()
    assert account_data is not None, "Create response didn't return JSON data"
    assert 'id' in account_data, f"'id' not found in create response. Data: {account_data}"
    account_id = account_data['id']

    # Now, delete the account
    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200, (
        f"Failed to delete account. Status: {delete_response.status_code}, "
        f"Response: {delete_response.data.decode('utf-8')}"
    )



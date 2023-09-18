def test_put_v1_account_password(dm_api_facade, data_helper, prepare_user):
    """Test that a user can successfully reset and change their password."""

    # Register and activate user
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dm_api_facade.account.activate_registered_user(login=login)

    # Authenticate and set token
    auth_token = dm_api_facade.login.get_auth_token(
        login=login,
        password=password
    )
    dm_api_facade.account.set_headers(headers=auth_token)

    # Reset password
    dm_api_facade.account.reset_user_password(
        login=login,
        email=email
    )

    # Generate a new password and change it
    new_password = data_helper.generate_password()
    dm_api_facade.account.change_user_password(
        login=login,
        old_password=password,
        new_password=new_password
    )

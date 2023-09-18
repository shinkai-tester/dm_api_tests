def test_put_v1_account_email(dm_api_facade, prepare_user, data_helper, assertions):
    """Test the process of changing a user's email and re-activating the account."""

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

    # Change user's email
    response_change_email = dm_api_facade.account.change_user_email(
        login=login,
        password=password,
        email=data_helper.generate_email()
    )
    assertions.assert_json_value_by_name(
        response=response_change_email,
        name="login",
        expected_value=login,
        error_message=f"User login is not as expected: {login}",
        path=["resource"]
    )

    # Reactivate user, as changing the email usually requires reactivation
    dm_api_facade.account.activate_registered_user(login=login)

def test_put_v1_account_token(dm_api_facade, data_helper, prepare_user, assertions):
    """
    Test the process of user registration and activation via token.
    """

    # Register the new user
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    dm_api_facade.account.register_new_user(
        login=login,
        password=password,
        email=email
    )

    # Activate the user using a token from their email
    response = dm_api_facade.account.activate_registered_user(
        login=login
    )

    assertions.assert_json_value_by_name(
        response=response,
        name="login",
        expected_value=login,
        error_message=f"User login is not equal to {login}",
        path=["resource"]
    )

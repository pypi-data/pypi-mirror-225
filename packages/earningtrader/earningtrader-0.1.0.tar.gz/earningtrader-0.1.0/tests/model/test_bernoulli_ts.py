import pytest

from earningtrader.model.bernoulli_ts import (
    BernTSTradingModel,
    BernTSState,
    BernTSAction,
)


def test_state_init_with_wrong_parameter_dimension():
    with pytest.raises(ValueError):
        assert (
            BernTSState(
                parameters_with_action_ids={"apple_id": [1], "msft_id": [3, 4]}
            )._parameters
            == 1
        )


def test_setting_parameter_correctly():
    state = BernTSState(
        parameters_with_action_ids={"apple_id": [1, 2], "msft_id": [3, 4]}
    )

    state.set_parameter(action_id="apple_id", reward=0.7)
    assert state._parameters[0].tolist() == [1.7, 2.3]


def test_setting_parameter_of_not_existing_action_id():
    state = BernTSState(
        parameters_with_action_ids={"apple_id": [1, 2], "msft_id": [3, 4]}
    )

    with pytest.raises(KeyError):
        state.set_parameter(action_id="tesla_id", reward=0.7)


def test_init_bern_ts_trading_model_with_unmatching_arguments():
    actions = set(
        [
            BernTSAction(id="apple_id", key="APPL"),
            BernTSAction(id="msft_id", key="MSFT"),
        ]
    )

    state = BernTSState(
        parameters_with_action_ids={"apple_id": [1, 2], "tesla_id": [3, 4]}
    )

    with pytest.raises(AssertionError):
        BernTSTradingModel(actions=actions, state=state)


def test_take_action():
    actions = set(
        [
            BernTSAction(id="apple_id", key="APPL"),
            BernTSAction(id="msft_id", key="MSFT"),
        ]
    )

    state = BernTSState(
        parameters_with_action_ids={"apple_id": [1, 2], "msft_id": [3, 4]}
    )

    trading_model = BernTSTradingModel(actions=actions, state=state)
    assert isinstance(trading_model, BernTSTradingModel)

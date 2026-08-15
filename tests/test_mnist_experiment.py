"""Tests for the MNIST experiment command."""

from digitrecognition import mnist_experiment


def test_main_runs_experiment_and_prints_results(
    monkeypatch,
    capsys,
):
    """The experiment should load data, evaluate it, and print results."""
    fake_images = [
        [
            [0 for _ in range(28)]
            for _ in range(28)
        ]
    ]
    fake_labels = [7]
    fake_training = [
        (
            7,
            [(0, 0)],
            [[True]],
        )
    ]
    fake_offsets = [(0, 0, 0.0)]

    monkeypatch.setattr(
        mnist_experiment,
        "load_mnist_images",
        lambda *args, **kwargs: fake_images,
    )
    monkeypatch.setattr(
        mnist_experiment,
        "load_mnist_labels",
        lambda *args, **kwargs: fake_labels,
    )
    monkeypatch.setattr(
        mnist_experiment,
        "prepare_training_images",
        lambda *args, **kwargs: fake_training,
    )
    monkeypatch.setattr(
        mnist_experiment,
        "generate_offsets",
        lambda *args, **kwargs: fake_offsets,
    )
    monkeypatch.setattr(
        mnist_experiment,
        "evaluate_classifier",
        lambda *args, **kwargs: (
            19,
            20,
            95.0,
            54.49,
        ),
    )

    mnist_experiment.main()

    output = capsys.readouterr().out

    assert "MNIST experiment results" in output
    assert "Training images: 1" in output
    assert "Test images: 20" in output
    assert "Threshold: 128" in output
    assert "k: 3" in output
    assert "Offset size: 11" in output
    assert "Distance measure: d22" in output
    assert "Correct predictions: 19/20" in output
    assert "Accuracy: 95.00%" in output
    assert "Elapsed time: 54.49 seconds" in output
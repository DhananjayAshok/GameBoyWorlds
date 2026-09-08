Adding a new task (given that the game is set up and the basic parser / tracker infra exists) is quite programmatic. Claude can do this effectively if you give it some essential details: 

Essential Details: 

1. Benchmark CSV information
- game, 
- task_name 
- init_state 
- state_tracker_class. state_tracker_class likely won't exist yet (it might), but this will let claude know what to call it in the registry. 

2. TerminationMetric Information: 
- What kind of termination mechanism is it (regionmatchtermination? any region matching termination?)
- required named screen regions and target names of captures to match against. 

3. Subgoal information (for each subgoal, in order)
- what is the name of the subgoal (will become )
- What kind of identification mechanism is it (AnyRegionMatch, regionmatch, etc)
- required name screens to match. 

Given this information, claude can do the rest. It must:

1. Verify that you have provided all the required info and error out if you haven't. 
2. Start by implementing the subgoals and test metric trackers in the appropriate module. For example for pokemon, it should look at src/gameboy_worlds/emulation/pokemon/test_metrics.py, read the reference implementations and then implement the subgoals and termination metrics with appropriate class names. 
3. Hook the test state tracker up with the right usage of make_subgoal_metric_class and TERMINATION_TRUNCATION_METRIC with an appropriate class name. Following the examples in src/gameboy_worlds/emulation/pokemon/trackers.py
4. Set up the state tracker in the registry. 
5. Use pandas read csv to pull in the existing game series benchmark csv and add a row of this to the csv and then use df.to_csv(, index=False) to save it back. For shifted_training_games and can_train_from_game, it should follow the example of other rows in the csv that match the exact same game in the series
6. Test that it works by running: `python demos/environment.py --game <game_name> --init_state <init_state> --state_tracker_class <state_tracker_class>` with debug_mode=False in project_params.yaml. If this fails, then either claude has made a mistake in the code, or, if the failure is related to not being able to find the .npy file in the storage directory expected location, then you have made a mistake and haven't saved the needed screen regions and claude should just tell you of this fact. 
7. Finally, it should give you the following command to test the benchmark task completion yourself: python demos/benchmark.py --game, --init_state and --state_tracker_class args filled out


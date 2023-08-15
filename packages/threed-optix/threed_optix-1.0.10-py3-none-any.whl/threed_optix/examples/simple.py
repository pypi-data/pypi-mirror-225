#!/usr/bin/env python3


import threed_optix.api as opt
import copy


def main():
    # create an instance of 'ThreedOptixAPI' passing your API key
    api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

    # get list of all your setups (in this stage 'Setup' objects have only 'name' and 'id' properties)
    setups = api.get_setups()
    print("setups:")
    for s in setups:
        print(f"\t{s}")
    print()

    # select some setup from the list
    setup = setups[0]

    # if you want just to run a simulation, you don't need to fetch setup details;
    # just call the 'run' method of the api object
    result = api.run(setup)

    # the 'AnalysisResult' object returned by the 'run' method has no actual data,
    # only the 'url' property pointing to where the data is stored in the cloud
    # use 'fetch' method of the api object to bring the data
    api.fetch(result)
    print("simulation result:")
    print(result.data)
    print()

    # you can save the data to the disk
    result.data.to_csv('rays.csv')

    # if you want to work with parts in the setup, you must fetch the setup
    # using the 'fetch' method of the api object (you guessed correctly)
    api.fetch(setup)
    print(f"parts in '{setup}' setup")
    for p in setup.parts:
        print(f"\t{p}")
    print()

    # now you can change properties of some part,
    # but don't forget to fetch it beforehand (see the pattern?)
    part = setup.parts[0]
    api.fetch(part)

    # we want to be able to restore our part to its original state after we done with our games,
    # so we make a deep copy of the part
    original_part = copy.deepcopy(part)

    # let's change the pose of the part
    print(f"pose of local '{part}' part:              {part.pose}")
    part.pose.position.x += 33.66
    part.pose.rotation = opt.Vector3(90, 0, 45)
    print(f"pose of local '{part}' part after change: {part.pose}")

    # great, now you moved and rotated the part;
    # but wait, this changed only your local copy of the part; let's update it in the cloud
    api.update(part)

    # just to make sure that the part was updated, we will fetch it again
    api.fetch(part)
    print(f"pose of '{part}' part in the cloud:       {part.pose}")

    # and finaly, lets restore our original part in the cloud
    api.update(original_part)


if __name__ == '__main__':
    main()

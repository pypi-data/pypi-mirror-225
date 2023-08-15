#!/usr/bin/env python3


import threed_optix.api as opt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def main():
    api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

    setups = api.get_setups()
    setup = [s for s in setups if s.name == 'setup_a'][0]
    print(f"working with '{setup}' setup")
    api.fetch(setup)

    part = setup.parts[1]
    print(f"finding the focal length of '{part}'")
    api.fetch(part)

    original_z = part.pose.position.z

    def run_simulation():
        result = api.run(setup)
        api.fetch(result)
        data = result.data
        data = data[data['hit_surface_idx'] == 3]
        return data

    fig, ax = plt.subplots(figsize=(10, 10))

    # to determine the ranges of axes
    data = run_simulation()
    minmax_x = (data['Hx'].min(), data['Hx'].max())
    minmax_y = (data['Hy'].min(), data['Hy'].max())

    areas = []
    z_positions = []
    n = 60

    def animate(i):
        ax.clear()

        print(f"running simulation for z position {part.pose.position.z} ({i+1} of {n})")
        data = run_simulation()

        ax.scatter(data['Hx'], data['Hy'])
        ax.set_title(f'z position = {part.pose.position.z}')
        ax.set_xlabel('Hx')
        ax.set_ylabel('Hy')
        ax.set_xlim(minmax_x[0], minmax_x[1])
        ax.set_ylim(minmax_y[0], minmax_y[1])

        z_positions.append(part.pose.position.z)
        area = (data['Hx'].max() - data['Hx'].min()) * (data['Hy'].max() - data['Hy'].min())
        areas.append(area)

        part.pose.position.z += 1
        api.update(part)

    anim = animation.FuncAnimation(fig, animate, frames=n)
    anim.save('spot.gif', writer='pillow')

    plt.close()

    min_area_index = areas.index(min(areas))
    print(f"z position of minimum area: {z_positions[min_area_index]}")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(z_positions, areas, markevery=[min_area_index], marker='o', ms=20, mec='r', mfc='None')
    ax.set_xlabel('z position')
    ax.set_ylabel('area')
    plt.show()

    part.pose.position.z = original_z
    api.update(part)


if __name__ == '__main__':
    main()

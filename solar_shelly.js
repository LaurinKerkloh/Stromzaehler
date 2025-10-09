//every 10 seconds
const interval = 10 * 1000;
const topic = "tele/Solar/SENSOR";

// wait to start timer on seconds % 10 = 0
const seconds_to_wait_for = 10 - (new Date().getSeconds() % 10);
Timer.set(seconds_to_wait_for * 1000, false, function () {
  // each interval send mqtt data
  Timer.set(interval, true, function () {
    // Get EM data
    const em = Shelly.getComponentStatus("em", 0);
    const emData = Shelly.getComponentStatus("emdata", 0);

    const totalPower = em.total_act_power; // Total active power (W)
    const totalEnergy = emData.total_act / 1000; // Total energy consumed (kWh)

    // Create JSON payload
    let payload = JSON.stringify({
      Time: new Date().toISOString().slice(0, 19),
      Solar: {
        reading: totalEnergy.toFixed(4),
        current_power: Math.round(totalPower),
      },
    });

    // Publish to MQTT
    MQTT.publish(topic, payload, 0, false);
  });
});

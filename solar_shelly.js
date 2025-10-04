const interval = 10000;
const topic = "tele/Solar/SENSOR";

Timer.set(interval, true, function () {
  // Get EM data
  let emData = Shelly.getComponentStatus("em", 0);

  if (emData) {
    let totalPower = emData.total_act_power; // Total active power (W)
    let totalEnergy = emData.total; // Total energy consumed (Wh)

    // Create JSON payload
    let payload = JSON.stringify({
      Time: new Date().toISOString(),
      Solar: {
        reading: totalEnergy,
        current_power: totalPower,
      },
    });

    // Publish to MQTT
    MQTT.publish("topic", payload, 0, false);

    console.log("MQTT ->", topic, payload);
  } else {
    console.log("Error: Unable to read EM data");
  }
});

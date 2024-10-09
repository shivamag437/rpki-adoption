(function () {
  // Set dimensions and margins for the chart
  const margin = { top: 70, right: 30, bottom: 40, left: 80 };
  const width = 1200 - margin.left - margin.right; // Adjust width to fit the selection box
  const height = 500 - margin.top - margin.bottom;

  // Parse the date/time
  const parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");

  // Set up the x and y scales
  const x = d3.scaleTime().range([0, width]);
  const y = d3.scaleLinear().range([height, 0]);

  // Create the SVG element and append it to the chart container
  const svg = d3.select("#invalids-asn-chart")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  d3.csv("Tier1ASes_IPv4_RPKIinvalidsCount_transposed.csv", d => {
      d.date = parseDate(d.date);
      for (let key in d) {
          if (key !== "date" && d[key] !== "NA") {
              d[key] = +d[key];  // Convert string to number
          } else if (d[key] === "NA") {
              d[key] = null; // Handle NA values
          }
      }
      return d;
  }).then(data => {
      const keys = data.columns.slice(1); // Get the columns (excluding date)
      const color = d3.scaleOrdinal(d3.schemeCategory10); // Color scale

      // Set the domains for the x and y scales
      x.domain(d3.extent(data, d => d.date));
      y.domain([0, d3.max(data, d => d3.max(keys, key => d[key]))]);

      // Add the x-axis
      svg.append("g")
          .attr("transform", `translate(0,${height})`)
          .style("font-size", "14px")
          .call(d3.axisBottom(x).tickValues(x.ticks(d3.timeMonth.every(6))).tickFormat(d3.timeFormat("%b %Y")))
          .selectAll(".tick line")
          .style("stroke-opacity", 0);

      svg.selectAll(".tick text").attr("fill", "#777");

      // Add the y-axis
      svg.append("g").style("font-size", "14px").call(d3.axisLeft(y));

      // Populate the ASN checkboxes
      const checkBoxContainer = d3.select("#asn-checkboxes");
      const selectedKeys = new Set(keys); // Track selected ASNs

      // Create checkboxes for each ASN
      keys.forEach((key) => {
          const checkboxDiv = checkBoxContainer.append("div").attr("class", "checkbox-container");

          // Create checkbox
          const checkbox = checkboxDiv.append("input")
              .attr("type", "checkbox")
              .attr("id", `asn-${key}`)
              .attr("checked", true) // Initially checked
              .on("change", function () {
                  if (this.checked) {
                      selectedKeys.add(key);
                  } else {
                      selectedKeys.delete(key);
                  }
                  updateChart(Array.from(selectedKeys)); // Update the chart with the new selection
              });

          // Create label for checkbox
          checkboxDiv.append("label")
              .attr("for", `asn-${key}`)
              .style("background-color", color(key))
              .style("padding", "5px")
              .style("border-radius", "4px")
              .style("margin", "5px")
              .style("display", "inline-block")
              .style("cursor", "pointer")
              .style("color", "#fff")
              .text(key);
      });

      // Function to update the chart
      function updateChart(selectedKeys) {
          svg.selectAll(".line").remove(); // Remove old lines
          svg.selectAll(".label").remove(); // Remove old labels

          // Draw lines for the selected ASNs
          selectedKeys.forEach((key) => {
              svg.append("path")
                  .datum(data)
                  .attr("fill", "none")
                  .attr("stroke", color(key))
                  .attr("stroke-width", 1.5)
                  .attr("class", "line")
                  .attr("d", d3.line().x(d => x(d.date)).y(d => y(d[key])));

              // Add labels for each line
              svg.append("text")
                  .attr("transform", `translate(${width},${y(data[data.length - 1][key])})`)
                  .attr("dy", "0.35em")
                  .style("font-size", "10px")
                  .style("fill", color(key))
                  .attr("class", "label")
                  .text(key);
          });
      }

      // Add event listener to the select/unselect all button
      let allSelected = true;
      d3.select("#toggle-select-all").on("click", function () {
          allSelected = !allSelected;
          d3.select(this).text(allSelected ? "Unselect All" : "Select All");

          // Update all checkboxes and the selectedKeys set
          checkBoxContainer.selectAll("input[type='checkbox']")
              .property("checked", allSelected)
              .each(function () {
                  const key = this.id.split("asn-")[1];
                  if (allSelected) {
                      selectedKeys.add(key);
                  } else {
                      selectedKeys.delete(key);
                  }
              });

          updateChart(Array.from(selectedKeys)); // Update the chart with new selection
      });

      // Initial chart update with all ASNs
      updateChart(keys);

      // Add the title for the chart
      svg.append("text")
          .attr("x", width / 2)
          .attr("y", 0 - (margin.top / 2))
          .attr("text-anchor", "middle")
          .style("font-size", "16px")
          .text("RPKI Invalids per ASN");

      // Add the Y-axis label
      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left)
          .attr("x", 0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .style("font-size", "14px")
          .text("# Of RPKI Invalid Routes");

  });
})();
